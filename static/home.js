import { apiRequest, showPopup } from "./utils.js";

export async function renderHome() {
  // --- General number formatter ---
  function formatNumber(num) {
    if (typeof num !== "number") {
      num = Number(num);
      if (isNaN(num)) return num;
    }
    return num.toLocaleString("en-US", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 1,
    });
  }

  // --- Users summary ---
  try {
    const { data } = await apiRequest("/api/users/summery");
    document.getElementById(
      "total-users"
    ).textContent = `Total Users: ${formatNumber(
      data?.user_count?.total_user || 0
    )}`;
    document.getElementById("roles-list").innerHTML = Array.isArray(
      data?.user_by_role
    )
      ? data.user_by_role
          .map((r) => `<li>${r.role}: ${formatNumber(r.total_user)}</li>`)
          .join("")
      : `<li>No role data available</li>`;
  } catch {
    showPopup("❌ Error fetching user summary.");
  }

  // --- Costs summary ---
  let costsSummary = {
    month: "N/A",
    total_spend: 0,
    total_costs: 0,
    avrage_spend: 0,
    highest_spend: 0,
    lowest_spend: 0,
  };
  try {
    const { summery: data } = await apiRequest("/api/costs/summery");
    if (data) costsSummary = data;
  } catch (err) {
    console.warn("⚠️ Using fallback for costs summary:", err.message);
  }

  document.getElementById(
    "month_name"
  ).textContent = `This Month: ${costsSummary.month}`;
  document.getElementById(
    "total-spend"
  ).textContent = `Total Spend: ${formatNumber(costsSummary.total_spend)}`;
  document.getElementById(
    "total-costs"
  ).textContent = `Total Costs: ${formatNumber(costsSummary.total_costs)}`;
  document.getElementById("avg-spend").textContent = `Avg Spend: ${formatNumber(
    costsSummary.avrage_spend
  )}`;
  document.getElementById("top-cost").textContent = `Top Cost: ${formatNumber(
    costsSummary.highest_spend
  )}`;
  document.getElementById(
    "lowest-cost"
  ).textContent = `Lowest Cost: ${formatNumber(costsSummary.lowest_spend)}`;

  // --- Salaries summary ---
  let salariesSummary = {
    month: "N/A",
    total_salary: 0,
    total_hour: 0,
    avg_hourly_rate: 0,
    total_record: 0,
  };
  let roles = [];
  try {
    const json = await apiRequest("/api/salaries/summery");
    if (json?.salaries_summery) salariesSummary = json.salaries_summery;
    if (Array.isArray(json?.salary_per_role)) roles = json.salary_per_role;
  } catch (err) {
    console.warn("⚠️ Using fallback for salaries summary:", err.message);
  }

  document.getElementById(
    "salary-month_name"
  ).textContent = `This Month: ${salariesSummary.month}`;
  document.getElementById(
    "salary-total-paid"
  ).textContent = `Total Paid: ${formatNumber(salariesSummary.total_salary)}`;
  document.getElementById(
    "salary-total-hours"
  ).textContent = `Total Hours: ${formatNumber(salariesSummary.total_hour)}`;
  document.getElementById(
    "salary-avg-rate"
  ).textContent = `Avg Hourly Rate: ${formatNumber(
    salariesSummary.avg_hourly_rate
  )}`;
  document.getElementById(
    "salary-record-count"
  ).textContent = `Salary Records: ${formatNumber(
    salariesSummary.total_record
  )}`;

  const roleTableBody = document.querySelector("#role-salary-table tbody");
  roleTableBody.innerHTML = roles.length
    ? roles
        .map(
          (r) => `
        <tr>
          <td>${r.role}</td>
          <td>${formatNumber(r.total_salary)}</td>
          <td>${formatNumber(r.avg_hourly_rate)}</td>
          <td>${formatNumber(r.total_hour)}</td>
        </tr>`
        )
        .join("")
    : `<tr><td colspan="4" class="text-center text-muted">No role-based salary data available</td></tr>`;

  // --- Combined Outcome ---
  const totalOutcome =
    (salariesSummary.total_salary || 0) + (costsSummary.total_spend || 0);
  const salaryPercent = totalOutcome
    ? ((salariesSummary.total_salary / totalOutcome) * 100).toFixed(1)
    : 0;
  const costPercent = totalOutcome
    ? ((costsSummary.total_spend / totalOutcome) * 100).toFixed(1)
    : 0;

  document.getElementById(
    "outcome-month"
  ).textContent = `This Month: ${salariesSummary.month}`;
  document.getElementById(
    "outcome-total"
  ).textContent = `Total Outcome (in toman): ${formatNumber(totalOutcome)}`;
  document.getElementById(
    "outcome-salaries"
  ).textContent = `Salaries: ${formatNumber(salariesSummary.total_salary)}`;
  document.getElementById("outcome-costs").textContent = `Costs: ${formatNumber(
    costsSummary.total_spend
  )}`;
  document.getElementById(
    "outcome-percent"
  ).textContent = `Breakdown: Salaries ${salaryPercent}% | Costs ${costPercent}%`;

  // --- Fetch summary data ---
  async function fetchData(entity, sy, sm, ey, em) {
    const base =
      entity === "costs"
        ? "/api/costs/monthly-range"
        : "/api/salaries/monthly-range";
    let query = `${base}?start_year=${sy}&end_year=${ey}`;
    if (sm && em) query += `&start_month=${sm}&end_month=${em}`;
    const res = await fetch(query);
    if (!res.ok) throw new Error("Network error");
    return res.json();
  }

  function renderTable(data) {
    const thead = document.querySelector("#dataTable thead");
    const tbody = document.querySelector("#dataTable tbody");

    if (!data || data.length === 0) {
      thead.innerHTML = "";
      tbody.innerHTML = "<tr><td>No data found</td></tr>";
      return;
    }

    const rows = Array.isArray(data?.data) ? data.data : data;
    const columns = Object.keys(rows[0]);

    thead.innerHTML =
      "<tr>" +
      columns
        .map((c) => {
          const key = c.toLowerCase();
          const isMoney =
            key.includes("salary") ||
            key.includes("spend") ||
            key.includes("cost") ||
            key.includes("total");
          return `<th>${c}${isMoney ? " (in toman)" : ""}</th>`;
        })
        .join("") +
      "<th>Action</th></tr>";

    tbody.innerHTML = rows
      .map((row) => {
        const cells = columns
          .map((c) => {
            const val = row[c];
            const isDateField = c === "year" || c === "month";
            return `<td>${
              typeof val === "number" && !isDateField ? formatNumber(val) : val
            }</td>`;
          })
          .join("");
        return `<tr>${cells}
        <td>
          <button class="btn btn-sm btn-primary detail-btn"
                  data-bs-toggle="modal"
                  data-bs-target="#detailModal"
                  data-year="${row.year}" data-month="${row.month}">
            Details
          </button>
        </td>
      </tr>`;
      })
      .join("");
  }

  document
    .getElementById("filterForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const entity = document.getElementById("entity").value;
      const sy = document.getElementById("startYear").value;
      const sm = document.getElementById("startMonth").value;
      const ey = document.getElementById("endYear").value;
      const em = document.getElementById("endMonth").value;

      if (!sy || !ey) {
        alert("Please enter start and end year");
        return;
      }

      try {
        const result = await fetchData(entity, sy, sm, ey, em);
        renderTable(result);
      } catch (err) {
        console.error(err);
        renderTable([]);
      }
    });

  async function fetchDetails(entity, year, month) {
    const base =
      entity === "costs"
        ? "/api/costs/monthly-cost"
        : "/api/salaries/monthly-salaries";
    const res = await fetch(`${base}?year=${year}&month=${month}`);
    if (!res.ok) throw new Error("Network error");
    return res.json();
  }

  function renderDetailTable(data) {
    const thead = document.querySelector("#detailTable thead");
    const tbody = document.querySelector("#detailTable tbody");

    if (!data || data.length === 0) {
      thead.innerHTML = "";
      tbody.innerHTML = "<tr><td>No data found</td></tr>";
      return;
    }

    const rows = Array.isArray(data?.data) ? data.data : data; // handle both shapes
    const columns = Object.keys(rows[0]);

    thead.innerHTML =
      "<tr>" +
      columns
        .map((c) => {
          const key = c.toLowerCase();
          const isMoney =
            key.includes("salary") ||
            key.includes("spend") ||
            key.includes("cost") ||
            key.includes("total");
          return `<th>${c}${isMoney ? " (in toman)" : ""}</th>`;
        })
        .join("") +
      "<th>Action</th></tr>";

    tbody.innerHTML = rows
      .map((row) => {
        const cells = columns
          .map((c) => {
            const val = row[c];
            const isDateField = c === "year" || c === "month";
            return `<td>${
              typeof val === "number" && !isDateField ? formatNumber(val) : val
            }</td>`;
          })
          .join("");
        return `<tr>${cells}
          <td>
            <button class="btn btn-sm btn-primary detail-btn"
                    data-bs-toggle="modal"
                    data-bs-target="#detailModal"
                    data-year="${row.year}" data-month="${row.month}">
              Details
            </button>
          </td>
        </tr>`;
      })
      .join("");
  }

  // --- Form submit to fetch and render summary table ---
  document
    .getElementById("filterForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const entity = document.getElementById("entity").value;
      const sy = document.getElementById("startYear").value;
      const sm = document.getElementById("startMonth").value;
      const ey = document.getElementById("endYear").value;
      const em = document.getElementById("endMonth").value;

      if (!sy || !ey) {
        alert("Please enter start and end year");
        return;
      }

      try {
        const result = await fetchData(entity, sy, sm, ey, em);
        renderTable(result);
      } catch (err) {
        console.error(err);
        renderTable([]);
      }
    });

  // --- Fetch details for modal ---
  async function fetchDetails(entity, year, month) {
    const base =
      entity === "costs"
        ? "/api/costs/monthly-cost"
        : "/api/salaries/monthly-salaries";
    const res = await fetch(`${base}?year=${year}&month=${month}`);
    if (!res.ok) throw new Error("Network error");
    return res.json(); // expects array
  }

  // --- Render detail table with unit labels (in toman) for money columns ---
  function renderDetailTable(data) {
    const thead = document.querySelector("#detailTable thead");
    const tbody = document.querySelector("#detailTable tbody");

    if (!data || data.length === 0) {
      thead.innerHTML = "";
      tbody.innerHTML = "<tr><td>No details found</td></tr>";
      return;
    }

    const cols = Object.keys(data[0]);

    thead.innerHTML =
      "<tr>" +
      cols
        .map((c) => {
          const key = c.toLowerCase();
          const isMoney =
            key.includes("salary") ||
            key.includes("spend") ||
            key.includes("cost") ||
            key.includes("amount") ||
            key.includes("rate") ||
            key.includes("total");
          return `<th>${c}${isMoney ? " (in toman)" : ""}</th>`;
        })
        .join("") +
      "</tr>";

    tbody.innerHTML = data
      .map(
        (row) =>
          "<tr>" +
          cols
            .map((c) => {
              const val = row[c];
              const isDateField = c === "year" || c === "month";
              return `<td>${
                typeof val === "number" && !isDateField
                  ? formatNumber(val)
                  : val
              }</td>`;
            })
            .join("") +
          "</tr>"
      )
      .join("");
  }

  // --- Bootstrap modal hook: load details on open ---
  const detailModal = document.getElementById("detailModal");
  detailModal.addEventListener("show.bs.modal", async (event) => {
    const button = event.relatedTarget;
    const year = button.getAttribute("data-year");
    const month = button.getAttribute("data-month");
    const entity = document.getElementById("entity").value;

    document.getElementById(
      "modalTitle"
    ).innerText = `Details for ${year}-${month}`;
    const details = await fetchDetails(entity, year, month);
    renderDetailTable(details);
  });
}
