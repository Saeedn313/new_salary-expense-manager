import { apiRequest, showPopup } from "./utils.js";

export async function renderHome() {
  // --- Users summary ---
  try {
    const { data } = await apiRequest("/api/users/summery");

    const totalUsersEl = document.getElementById("total-users");
    if (totalUsersEl) {
      totalUsersEl.textContent = `Total Users: ${data.user_count.total_user}`;
    }

    const roleListEl = document.getElementById("roles-list");
    if (roleListEl) {
      roleListEl.innerHTML = data.user_by_role
        .map((role) => `<li>${role.role}: ${role.total_user}</li>`)
        .join("");
    }
  } catch {
    showPopup("❌ Error fetching user summary.");
  }

  // --- Costs summary ---
  try {
    const { summery: data } = await apiRequest("/api/costs/summery");
    const format = (num) => num.toLocaleString("en-US");

    document.getElementById("total-spend").textContent = `Total Spend: ${format(
      data.total_spend
    )}`;
    document.getElementById(
      "total-costs"
    ).textContent = `Total Costs ${data.total_costs}`;
    document.getElementById("avg-spend").textContent = `Avg Spend: ${format(
      data.avrage_spend
    )}`;
    document.getElementById("top-cost").textContent = `Top Cost: ${format(
      data.highest_spend
    )}`;
    document.getElementById("lowest-cost").textContent = `Lowest Cost: ${format(
      data.lowest_spend
    )}`;
  } catch {
    showPopup("❌ Error fetching cost summary.");
  }

  // --- Monthly average button ---
  document
    .getElementById("get-monthly-avg")
    .addEventListener("click", async () => {
      const month = document.getElementById("avg-month").value;
      const year = document.getElementById("avg-year").value;

      if (!month || !year) {
        showPopup("⚠️ Please enter both month and year.");
        return;
      }

      try {
        const data = await apiRequest(
          `/api/costs/monthly-costs-avg?year=${year}&month=${month}`
        );
        document.getElementById(
          "monthly-average"
        ).textContent = `In year ${data.year}, month ${data.month}, the avg is ${data.avg_spend}`;
      } catch {
        document.getElementById(
          "monthly-average"
        ).textContent = `No data found for year ${year}, month ${month}.`;
      }
    });

  // --- Costs table ---
  const tableBody = document.querySelector("#cost-table tbody");
  function renderCosts(costs) {
    if (!costs || costs.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="4">No data found.</td></tr>`;
      return;
    }
    tableBody.innerHTML = costs
      .map(
        (c, i) => `
      <tr>
        <td>${i + 1}</td>
        <td>${c.amount}</td>
        <td>${c.year}</td>
        <td>${c.month}</td>
      </tr>
    `
      )
      .join("");
  }

  // Toggle range form
  document.getElementById("show-range-form").addEventListener("click", () => {
    const form = document.getElementById("range-form");
    form.style.display = form.style.display === "none" ? "flex" : "none";
  });

  // Fetch filtered costs by range
  document.getElementById("fetch-range").addEventListener("click", async () => {
    const startYear = document.getElementById("start-year").value;
    const startMonth = document.getElementById("start-month").value;
    const endYear = document.getElementById("end-year").value;
    const endMonth = document.getElementById("end-month").value;

    if (!startYear || !endYear) {
      showPopup("⚠️ Please fill in all range fields.");
      return;
    }

    let query = `/api/costs/monthly-range?start_year=${startYear}&end_year=${endYear}`;
    if (startMonth && endMonth) {
      query += `&start_month=${startMonth}&end_month=${endMonth}`;
    }

    try {
      const { data } = await apiRequest(query);
      renderCosts(data);
    } catch {
      tableBody.innerHTML = `<tr><td colspan="4">Error fetching filtered data.</td></tr>`;
    }
  });

  // --- Salaries summary ---
  try {
    const json = await apiRequest("/api/salaries/summery");
    const summary = json.salaries_summery;
    const roles = json.salary_per_role;
    const format = (num) => num.toLocaleString("en-US");

    document.getElementById(
      "salary-total-paid"
    ).textContent = `Total Paid: $${format(summary.total_salary)}`;
    document.getElementById(
      "salary-total-hours"
    ).textContent = `Total Hours: ${format(summary.total_hour)}`;
    document.getElementById(
      "salary-avg-rate"
    ).textContent = `Avg Hourly Rate: $${format(summary.avg_hourly_rate)}`;
    document.getElementById(
      "salary-record-count"
    ).textContent = `Salary Records: ${summary.total_record}`;

    const roleTableBody = document.querySelector("#role-salary-table tbody");
    roleTableBody.innerHTML = roles
      .map(
        (role) => `
      <tr>
        <td>${role.role}</td>
        <td>${format(role.total_salary)}</td>
        <td>${format(role.avg_hourly_rate)}</td>
        <td>${format(role.total_hour)}</td>
      </tr>
    `
      )
      .join("");
  } catch {
    showPopup("❌ Error fetching salary summary.");
  }

  // Toggle salary range form
  document
    .getElementById("toggle-salary-form")
    .addEventListener("click", () => {
      const form = document.getElementById("salary-range-form");
      const btn = document.getElementById("toggle-salary-form");
      if (form.style.display === "none") {
        form.style.display = "flex";
        btn.textContent = "❌ Hide Salary Range Filter";
      } else {
        form.style.display = "none";
        btn.textContent = "🔍 Show Salary Range Filter";
      }
    });

  // Fetch salary range data
  async function fetchSalaryRange(startYear, startMonth, endYear, endMonth) {
    let query = `/api/costs/monthly-range?start_year=${startYear}&end_year=${endYear}`;
    if (startMonth && endMonth) {
      query += `&start_month=${startMonth}&end_month=${endMonth}`;
    }
    try {
      const { data: rows } = await apiRequest(query);
      const format = (num) => num.toLocaleString("en-US");
      const tbody = document.querySelector("#salary-table tbody");
      tbody.innerHTML = rows
        .map(
          (r) => `
        <tr>
          <td>${r.year}</td>
          <td>${r.month}</td>
          <td>$${format(r.amount)}</td>
        </tr>
      `
        )
        .join("");
    } catch {
      showPopup("❌ Error fetching salary range.");
    }
  }

  document
    .getElementById("fetch-salary-range")
    .addEventListener("click", () => {
      const startYear = document.getElementById("salary-start-year").value;
      const startMonth = document.getElementById("salary-start-month").value;
      const endYear = document.getElementById("salary-end-year").value;
      const endMonth = document.getElementById("salary-end-month").value;

      if (startYear && endYear) {
        fetchSalaryRange(startYear, startMonth, endYear, endMonth);
      } else {
        showPopup("⚠️ Please fill in all fields for year and month range.");
      }
    });
}
