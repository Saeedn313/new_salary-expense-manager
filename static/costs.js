import { handleLocation } from "./app.js";
import { apiRequest, formToJSON, showPopup } from "./utils.js";

function renderCostTable(costs) {
  const format = (num) => num.toLocaleString("en-US");
  return costs
    .map(
      (cost) => `
    <tr>
      <td>${cost.description}</td>
      <td>${format(cost.amount)}</td>
      <td>${cost.year}</td>
      <td>${cost.month}</td>
      <td>
        <button data-id="${cost.id}" class="delete-cost-btn">Delete</button>
        <button class="edit-cost-btn"
          data-id="${cost.id}"
          data-description="${cost.description}"
          data-amount="${cost.amount}"
          data-year="${cost.year}"
          data-month="${cost.month}"
        >Edit</button>
      </td> 
    </tr>
  `
    )
    .join("");
}

export async function renderCosts() {
  const list = document.getElementById("cost-list");

  try {
    const data = await apiRequest("/api/costs/");
    const costs = Array.isArray(data) ? data : data.costs;
    list.innerHTML = renderCostTable(costs);
  } catch (err) {
    list.innerHTML = `<tr><td colspan="5">Failed to load costs</td></tr>`;
    showPopup(err.message, "error");
    return;
  }

  // Edit buttons
  document.querySelectorAll(".edit-cost-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById("edit_cost_id").value = btn.dataset.id;
      document.getElementById("edit_description").value =
        btn.dataset.description;
      document.getElementById("edit_amount").value = btn.dataset.amount;
      document.getElementById("edit_year").value = btn.dataset.year;
      document.getElementById("edit_month").value = btn.dataset.month;
      document.getElementById("edit-cost-form").style.display = "block";
    });
  });

  // Hide edit form
  window.hideEditForm = function () {
    document.getElementById("edit-cost-form").style.display = "none";
    document.getElementById("update-cost-form").reset();
  };

  // Update cost form
  document
    .getElementById("update-cost-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();
      const json = Object.fromEntries(new FormData(this).entries());
      const costId = json.cost_id;

      try {
        await apiRequest(`/api/costs/update-cost/${costId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(json),
        });
        showPopup("✅ Cost updated successfully", "success");
        window.history.pushState({}, "", "/costs");
        handleLocation();
      } catch (err) {
        showPopup(err.message, "error");
      }
    });

  // Delete buttons
  document.querySelectorAll(".delete-cost-btn").forEach((btn) => {
    btn.addEventListener("click", async function () {
      const costId = this.dataset.id;
      try {
        await apiRequest(`/api/costs/delete-cost/${costId}`, {
          method: "DELETE",
        });
        showPopup("✅ Cost deleted successfully", "success");
        window.history.pushState({}, "", "/costs");
        handleLocation();
      } catch (err) {
        showPopup(err.message, "error");
      }
    });
  });

  // Add cost form
  document
    .getElementById("add-cost-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();
      try {
        await apiRequest("/api/costs/add-cost", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: formToJSON(e.target),
        });
        showPopup("✅ Cost added successfully", "success");
        window.history.pushState({}, "", "/costs");
        handleLocation();
      } catch (err) {
        showPopup(err.message, "error");
      }
    });
}
