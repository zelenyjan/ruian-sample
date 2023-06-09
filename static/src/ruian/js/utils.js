export function getCookie(name) {
  // get cookie by name

  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function getCSRFToken() {
  // get csrf cookie
  return getCookie("csrftoken");
}

export const axiosConfig = {
  headers: {
    "X-CSRFToken": getCSRFToken(),
  },
};
