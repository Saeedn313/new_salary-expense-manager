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
    // Load specific user profile
    try {
      const res = await fetch(`/api/users/${userId}`);
      const data = await res.json();
      const user = data.user;
      console.log(user);

      const profile = document.getElementById("user-profile");
      profile.innerHTML = `
        <p><strong>ID:</strong> ${user.id}</p>
        <p><strong>Name:</strong> ${user.name}</p>
        <p><strong>Family:</strong> ${user.family}</p>
        <p><strong>Role:</strong> ${user.role}</p>
      `;

      // Later you can add forms to #user-actions
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
