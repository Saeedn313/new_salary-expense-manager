import { handleLocation } from "./app.js";
import { apiRequest, formToJSON, showPopup } from "./utils.js";

export async function renderProfilePage(userId) {
  try {
    const data = await apiRequest(`/api/users/${userId}`);
    const user = data.user;

    const profile = document.getElementById("user-profile");
    profile.innerHTML = `
      <p><strong>ID:</strong> ${user.id}</p>
      <p><strong>Name:</strong> ${user.name}</p>
      <p><strong>Family:</strong> ${user.family}</p>
      <p><strong>Role:</strong> ${user.role}</p>
      <p><strong>Role:</strong> ${user.created_at}</p>
    `;

    document.getElementById("update_user_id").value = userId;
    document.getElementById("name").value = user.name || "";
    document.getElementById("family").value = user.family || "";
    document.getElementById("role").value = user.role || "";

    document
      .getElementById("update-user-form")
      .addEventListener("submit", async function (e) {
        e.preventDefault();
        const json = Object.fromEntries(new FormData(this).entries());
        const updateUserId = json.user_id;

        try {
          await apiRequest(`/api/users/update-user/${updateUserId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(json),
          });
          showPopup("✅ User updated successfully", "success");
          window.history.pushState({}, "", `/users/${userId}`);
          handleLocation();
        } catch (err) {
          showPopup(err.message, "error");
        }
      });

    document.getElementById("salary_user_id").value = userId;
    document
      .getElementById("add-salary-form")
      .addEventListener("submit", async function (e) {
        e.preventDefault();
        try {
          await apiRequest("/api/salaries/add-salary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: formToJSON(this),
          });
          showPopup("✅ Salary added successfully", "success");
          window.history.pushState({}, "", `/users/${userId}`);
          handleLocation();
        } catch (err) {
          showPopup(err.message, "error");
        }
      });

    try {
      const salaryData = await apiRequest(`/api/salaries/${userId}`);
      const salaries = Array.isArray(salaryData)
        ? salaryData
        : salaryData.salaries;
      const format = (num) => num.toLocaleString("en-US");

      const list = document.getElementById("salary_list");
      list.innerHTML = salaries
        .map(
          (salary) => `
        <tr>
          <td>${salary.year}</td>
          <td>${salary.month}</td>
          <td>${format(salary.hourly_rate)}</td>
          <td>${salary.total_hour}</td>
          <td>${salary.total_min}</td>
          <td>${format(salary.total_salary)}</td>
          <td>
            <button data-id="${
              salary.id
            }" class="delete-salary-btn">Delete</button>
            <button class="edit-salary-btn"
              data-salary-id="${salary.id}"
              data-user-id="${salary.user_id}"
              data-year="${salary.year}"
              data-month="${salary.month}"
              data-hourly-rate="${salary.hourly_rate}"
              data-total-hour="${salary.total_hour}"
              data-total-min="${salary.total_min}"
            >Edit</button>
          </td>
        </tr>
      `
        )
        .join("");

      document.querySelectorAll(".edit-salary-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          document.getElementById("edit_salary_id").value =
            btn.dataset.salaryId;
          document.getElementById("edit_user_id").value = btn.dataset.userId;
          document.getElementById("edit_year").value = btn.dataset.year;
          document.getElementById("edit_month").value = btn.dataset.month;
          document.getElementById("edit_hourly_rate").value =
            btn.dataset.hourlyRate;
          document.getElementById("edit_total_hour").value =
            btn.dataset.totalHour;
          document.getElementById("edit_total_min").value =
            btn.dataset.totalMin;
          document.getElementById("edit-salary-form").style.display = "block";
        });
      });

      window.hideEditForm = function () {
        document.getElementById("edit-salary-form").style.display = "none";
        document.getElementById("update-salary-form").reset();
      };

      document
        .getElementById("update-salary-form")
        .addEventListener("submit", async function (e) {
          e.preventDefault();
          const json = Object.fromEntries(new FormData(this).entries());
          const salaryId = json.salary_id;

          try {
            await apiRequest(`/api/salaries/update-salary/${salaryId}`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(json),
            });
            showPopup("✅ Salary updated successfully", "success");
            window.history.pushState({}, "", `/users/${userId}`);
            handleLocation();
          } catch (err) {
            showPopup(err.message, "error");
          }
        });

      document.querySelectorAll(".delete-salary-btn").forEach((btn) => {
        btn.addEventListener("click", async function () {
          const salaryId = this.dataset.id;
          try {
            await apiRequest(`/api/salaries/delete-salary/${salaryId}`, {
              method: "POST",
            });
            showPopup("✅ Salary deleted successfully", "success");
            window.history.pushState({}, "", `/users/${userId}`);
            handleLocation();
          } catch (err) {
            showPopup(err.message, "error");
          }
        });
      });
    } catch (err) {
      document.getElementById("salary_list").innerHTML = `
        <tr><td colspan="7">Failed to load salaries</td></tr>
      `;
      showPopup(err.message, "error");
    }
  } catch (err) {
    document.getElementById("user-profile").innerHTML = `<p>User not found</p>`;
    showPopup(err.message, "error");
  }
}
