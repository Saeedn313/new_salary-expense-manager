import { renderUsers } from "./users.js";
import { renderCosts } from "./costs.js";
import { renderProfilePage } from "./userProfile.js";
import { renderHome } from "./home.js"

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

export const handleLocation = async () => {
  const path = window.location.pathname;
  const userId = path.startsWith("/users/") ? path.split("/")[2] : null;
  const route =
    routes[path] || (userId ? "/static/user_profile.html" : routes[404]);

  const html = await fetch(route).then((data) => data.text());
  document.getElementById("app").innerHTML = html;

  if (path == "/") {
    renderHome();
  }
  if (path === "/users") {
    renderUsers();
  }
  if (path == "/costs") {
    renderCosts();
  }
  if (userId) {
    renderProfilePage(userId);
  }
};
window.onpopstate = handleLocation;
window.route = route;

handleLocation();
