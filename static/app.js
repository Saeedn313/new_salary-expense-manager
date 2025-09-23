const route = (event) => {
  event = event || window.event;
  event.preventDefault();
  window.history.pushState({}, "", event.target.href);
  handleLocation();
};

const routes = {
  404: "/static/404.html",
  "/": "/static/home.html",
  "/users": "/static/users.html",
  "/costs": "/static/costs.html",
};

const handleLocation = async () => {
  const path = window.location.pathname;
  const userId = path.startsWith("/users/") ? path.split("/")[2] : null;
  const route =
    routes[path] || (userId ? "/static/user_profile.html" : routes[404]);

  const html = await fetch(route).then((data) => data.text());
  document.getElementById("app").innerHTML = html;

  if (path == "/") {
    try {
      const res = await fetch("/api/users/summery");
      const json = await res.json();
      const data = json.data;

      const totalUsersEl = document.getElementById("total-users");
      if (totalUsersEl) {
        totalUsersEl.textContent = `Total Users: ${data.user_count.total_user}`;
      }

      const roleListEl = document.getElementById("roles-list");
      if (roleListEl) {
        roleListEl.innerHTML = "";
        data.user_by_role.forEach((role) => {
          const li = document.createElement("li");
          li.textContent = `${role.role}: ${role.total_user}`;
          roleListEl.appendChild(li);
        });
      }
    } catch (err) {
      console.error("Error fetching user summary:", err);
    }
    try {
      const res = await fetch("/api/costs/summery");
      const json = await res.json();
      const data = json.summery;
      console.log(data);

      const format = (num) => num.toLocaleString("en-US");

      document.getElementById(
        "total-spend"
      ).textContent = `Total Spend: ${format(data.total_spend)}`;

      document.getElementById(
        "avg-spend"
      ).textContent = `Avg Monthly Spend: ${format(data.avrage_spend)}`;

      document.getElementById("top-cost").textContent = `Top Cost: ${format(
        data.highest_spend
      )}`;

      document.getElementById(
        "lowest-cost"
      ).textContent = `Lowest Cost: ${format(data.lowest_spend)}`;
    } catch (err) {
      console.error("Error fetching cost summary:", err);
    }
  }

  if (path === "/users") {
    // Load all users
    try {
      const res = await fetch("/api/users/");
      const data = await res.json();
      const users = Array.isArray(data) ? data : data.users;
      const list = document.getElementById("user-list");

      let html = "";
      users.forEach((user) => {
        html += `
          <tr>
            <td><a href="/users/${user.id}" onclick="route(event)">${user.id}</a></td>
            <td>${user.name}</td>
            <td>${user.family}</td>
            <td>${user.role}</td>
            <td><button data-id="${user.id}" class="delete-user-btn">Delete</button></td>
          </tr>
        `;
      });

      list.innerHTML = html;
      document.querySelectorAll(".delete-user-btn").forEach((btn) => {
        btn.addEventListener("click", async function () {
          const userId = this.getAttribute("data-id");

          try {
            const res = await fetch(`/api/users/delete-user/${userId}`, {
              method: "Delete",
            });

            if (res.ok) {
              // Refresh the /users page
              window.history.pushState({}, "", "/users");
              handleLocation();
            } else {
              console.error("Failed to delete user:", await res.text());
            }
          } catch (err) {
            console.error("Error deleting user:", err);
          }
        });
      });
    } catch (err) {
      console.error("Error fetching users:", err);
      document.getElementById("user-list").innerHTML = `
        <tr><td colspan="4">Failed to load users</td></tr>
      `;
    }
    document
      .getElementById("add-user-form")
      .addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const json = Object.fromEntries(formData.entries());

        try {
          const res = await fetch("/api/users/add-user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(json),
          });

          if (res.ok) {
            window.history.pushState({}, "", "/users");
            handleLocation();
          } else {
            console.error("Failed to add user:", await res.text());
          }
        } catch (err) {
          console.error("Error submitting form:", err);
        }
      });
  }

  if (path == "/costs") {
    try {
      const res = await fetch("/api/costs/");
      const data = await res.json();
      const costs = Array.isArray(data) ? data : data.costs;
      const list = document.getElementById("cost-list");

      let html = "";
      costs.forEach((cost) => {
        console.log(cost);
        html += `
          <tr>
            <td>${cost.description}</td>
            <td>${cost.amount}</td>
            <td>${cost.year}</td>
            <td>${cost.month}</td>
            <td><button data-id="${cost.id}" class="delete-cost-btn">Delete</button>
            <button class="edit-cost-btn"
          data-id="${cost.id}"
          data-description="${cost.description}"
          data-amount="${cost.amount}"
          data-year="${cost.year}"
          data-month="${cost.month}"
        >Edit</button>
            </td> 
          </tr>
        `;
      });
      list.innerHTML = html;
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

      window.hideEditForm = function () {
        document.getElementById("edit-cost-form").style.display = "none";
        document.getElementById("update-cost-form").reset();
      };

      document
        .getElementById("update-cost-form")
        .addEventListener("submit", async function (e) {
          e.preventDefault();

          const formData = new FormData(this);
          const json = Object.fromEntries(formData.entries());
          const costId = json.cost_id;

          try {
            const res = await fetch(`/api/costs/update-cost/${costId}`, {
              method: "Post",
              headers: { "Content-type": "application/json" },
              body: JSON.stringify(json),
            });

            if (res.ok) {
              window.history.pushState({}, "", "/costs");
              handleLocation();
            } else {
              console.error("Failed to update cost: ", await res.text());
            }
          } catch (err) {
            console.error("Error updating cost", err);
          }
        });

      document.querySelectorAll(".delete-cost-btn").forEach((btn) => {
        btn.addEventListener("click", async function () {
          const costId = this.getAttribute("data-id");

          try {
            const res = await fetch(`/api/costs/delete-cost/${costId}`, {
              method: "Delete",
            });
            if (res.ok) {
              window.history.pushState({}, "", "/costs");
              handleLocation();
            } else {
              console.log("Failed to delete cost: ", await res.text());
            }
          } catch (err) {
            console.error("Error in deleting cost: ", err);
          }
        });
      });
    } catch (err) {
      console.error("Error fetching costs:", err);
      document.getElementById("cost-list").innerHTML = `
        <tr><td colspan="4">Failed to load costs</td></tr>
      `;
    }
    document
      .getElementById("add-cost-form")
      .addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const json = Object.fromEntries(formData.entries());

        try {
          const res = await fetch("/api/costs/add-cost", {
            method: "Post",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify(json),
          });

          if (res.ok) {
            window.history.pushState({}, "", "/costs");
            handleLocation();
          } else {
            console.error("Failed to add cost: ", await res.text());
          }
        } catch (err) {
          console.error("error submitting form: ", err);
        }
      });
  }

  if (userId) {
    try {
      // Fetch and render user profile
      const res = await fetch(`/api/users/${userId}`);
      const data = await res.json();
      const user = data.user;

      const profile = document.getElementById("user-profile");
      profile.innerHTML = `
      <p><strong>ID:</strong> ${user.id}</p>
      <p><strong>Name:</strong> ${user.name}</p>
      <p><strong>Family:</strong> ${user.family}</p>
      <p><strong>Role:</strong> ${user.role}</p>
    `;

      // Pre-fill update form
      document.getElementById("update_user_id").value = userId;
      document.getElementById("name").value = user.name || "";
      document.getElementById("family").value = user.family || "";
      document.getElementById("role").value = user.role || "";

      // Update user form submit
      document
        .getElementById("update-user-form")
        .addEventListener("submit", async function (e) {
          e.preventDefault();
          const formData = new FormData(this);
          const json = Object.fromEntries(formData.entries());
          const updateUserId = json.user_id;

          try {
            const res = await fetch(`/api/users/update-user/${updateUserId}`, {
              method: "POST",
              headers: { "Content-type": "application/json" },
              body: JSON.stringify(json),
            });

            if (res.ok) {
              window.history.pushState({}, "", `/users/${userId}`);
              handleLocation();
            } else {
              console.error("Failed to update user", await res.text());
            }
          } catch (err) {
            console.error("Error updating user", err);
          }
        });

      // Add salary form submit
      document.getElementById("salary_user_id").value = userId;
      document
        .getElementById("add-salary-form")
        .addEventListener("submit", async function (e) {
          e.preventDefault();
          const formData = new FormData(this);
          const json = Object.fromEntries(formData.entries());

          try {
            const res = await fetch("/api/salaries/add-salary", {
              method: "POST",
              headers: { "Content-type": "application/json" },
              body: JSON.stringify(json),
            });

            if (res.ok) {
              window.history.pushState({}, "", `/users/${userId}`);
              handleLocation();
            } else {
              console.error("Failed to add salary", await res.text());
            }
          } catch (err) {
            console.error("Error adding salary", err);
          }
        });

      // Fetch and render salaries in a separate try/catch
      try {
        const salaryRes = await fetch(`/api/salaries/${userId}`);
        if (!salaryRes.ok) throw new Error(await salaryRes.text());

        const salaryData = await salaryRes.json();
        const salaries = Array.isArray(salaryData)
          ? salaryData
          : salaryData.salaries;

        const list = document.getElementById("salary_list");
        let html = "";

        salaries.forEach((salary) => {
          html += `
    <tr>
      <td>${salary.year}</td>
      <td>${salary.month}</td>
      <td>${salary.hourly_rate}</td>
      <td>${salary.total_hour}</td>
      <td>${salary.total_min}</td>
      <td>${salary.total_salary}</td>
      <td>
        <button data-id="${salary.id}" class="delete-salary-btn">Delete</button>
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
  `;
        });

        list.innerHTML = html;

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

            const formData = new FormData(this);
            const json = Object.fromEntries(formData.entries());
            const salaryId = json.salary_id;

            try {
              const res = await fetch(
                `/api/salaries/update-salary/${salaryId}`,
                {
                  method: "POST",
                  headers: { "Content-type": "application/json" },
                  body: JSON.stringify(json),
                }
              );

              if (res.ok) {
                window.history.pushState({}, "", `/users/${userId}`);
                handleLocation();
              } else {
                console.error("Failed to update cost: ", await res.text());
              }
            } catch (err) {
              console.error("Error updating cost", err);
            }
          });

        // Attach delete handlers
        document.querySelectorAll(".delete-salary-btn").forEach((btn) => {
          btn.addEventListener("click", async function () {
            const salaryId = this.getAttribute("data-id");

            try {
              const res = await fetch(
                `/api/salaries/delete-salary/${salaryId}`,
                {
                  method: "POST",
                }
              );

              if (res.ok) {
                window.history.pushState({}, "", `/users/${userId}`);
                handleLocation();
              } else {
                console.error("Failed to delete salary:", await res.text());
              }
            } catch (err) {
              console.error("Error deleting salary:", err);
            }
          });
        });
      } catch (err) {
        console.error("Error fetching salaries:", err);
        document.getElementById("salary_list").innerHTML = `
        <tr><td colspan="7">Failed to load salaries</td></tr>
      `;
      }
    } catch (err) {
      console.error("Error loading user profile:", err);
      document.getElementById("user-profile").innerHTML = `
      <p>User not found</p>
    `;
    }
  }
};

window.onpopstate = handleLocation;
window.route = route;

handleLocation();
