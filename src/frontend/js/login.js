document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    fetch(IP_API + "/token", {
        method: "POST",
        headers: {
            accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params.toString(),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })

        .then((data) => {
            const access_token = data.access_token;
            const token_type = data.token_type;
            const user_id = data.user_id;
            const username = data.username;

            console.log("access_token:", access_token);
            console.log("token_type:", token_type);
            console.log("user_id:", user_id);
            console.log("username:", username);

            localStorage.setItem("access_token", access_token);
            // window.location.href = '../html/test.html';
            window.location.href = '/';
        })

        .catch((error) => {
            console.error("Ошибка:", error);
            alert("Возможно такого пользователя не существует");
        });
});
