// utils.js
export async function apiRequest(url, options = {}) {
  try {
    const res = await fetch(url, options);

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText || `Request failed with ${res.status}`);
    }

    const contentType = res.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return await res.json();
    } else {
      return await res.text();
    }
  } catch (err) {
    console.error("API request error:", err);
    throw err;
  }
}

export function formToJSON(form) {
  const formData = new FormData(form);
  return JSON.stringify(Object.fromEntries(formData.entries()));
}

export function showPopup(message, type = "success") {
  const typeStyles = {
    success: { background: "#52c41a", color: "#fff" }, // green
    error: { background: "#ff4d4f", color: "#fff" }, // red
    warning: { background: "#faad14", color: "#fff" }, // orange
    info: { background: "#1890ff", color: "#fff" }, // blue
    neutral: { background: "#f0f0f0", color: "#333" }, // light gray
  };

  const style = typeStyles[type] || typeStyles.neutral;

  let popup = document.getElementById("popup");
  if (!popup) {
    popup = document.createElement("div");
    popup.id = "popup";
    popup.style.position = "fixed";
    popup.style.top = "20px";
    popup.style.right = "20px";
    popup.style.padding = "12px 18px";
    popup.style.borderRadius = "6px";
    popup.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
    popup.style.zIndex = "1000";
    popup.style.fontWeight = "bold";
    popup.style.fontSize = "1em";
    popup.style.maxWidth = "300px";
    popup.style.wordWrap = "break-word";
    document.body.appendChild(popup);
  }

  popup.textContent = message;
  popup.style.background = style.background;
  popup.style.color = style.color;
  popup.style.display = "block";

  setTimeout(() => {
    popup.style.display = "none";
  }, 3000);
}
