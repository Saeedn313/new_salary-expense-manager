import { handleLocation } from "./app.js";
import { apiRequest, formToJSON, showPopup } from "./utils.js";

function renderUserTable(users) {
  return users
    .map(
      (user) => `
    <tr>
      <td><a href="/users/${user.id}" onclick="route(event)">${user.id}</a></td>
      <td>${user.name}</td>
      <td>${user.family}</td>
      <td>${user.role}</td>
      <td class="text-end">
        <button 
          data-id="${user.id}" 
          class="btn btn-sm btn-danger delete-user-btn">
          🗑️ Delete
        </button>
      </td>
    </tr>
  `
    )
    .join("");
}

export async function renderUsers() {
  const list = document.getElementById("user-list");

  try {
    const data = await apiRequest("/api/users/");
    const users = Array.isArray(data) ? data : data.users;
    list.innerHTML = renderUserTable(users);
  } catch (err) {
    list.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Failed to load users</td></tr>`;
    showPopup(err.message, "error");
    return;
  }

  // Event delegation for delete
  list.addEventListener("click", async (e) => {
    if (e.target.classList.contains("delete-user-btn")) {
      const userId = e.target.dataset.id;
      try {
        await apiRequest(`/api/users/delete-user/${userId}`, {
          method: "DELETE",
        });
        showPopup("✅ User deleted successfully", "success");
        window.history.pushState({}, "", "/users");
        handleLocation();
      } catch (err) {
        showPopup(err.message, "error");
      }
    }
  });

  // Add user form
  document
    .getElementById("add-user-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        await apiRequest("/api/users/add-user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: formToJSON(e.target),
        });
        showPopup("✅ User added successfully", "success");
        window.history.pushState({}, "", "/users");
        handleLocation();
      } catch (err) {
        showPopup(err.message, "error");
      }
    });
}
