document.addEventListener("DOMContentLoaded", function () {
    fetchUserInfo();
});

function fetchUserInfo() {
    const accessToken = localStorage.getItem('token'); // Token'ı al

    fetch('/simple_user_info', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP hata! Durum: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if(document.getElementById('userInfo')) {
            document.getElementById('userInfo').textContent = data.username;
        }
        
        
        document.getElementById('balance').textContent = `Bakiye: ${data.balance}₺`;
    })
    .catch(error => {
        console.error('API verisi alınırken hata oluştu:', error);
        document.getElementById('userInfo').textContent = 'Kullanıcı bilgileri yüklenemedi';
        document.getElementById('balance').textContent = 'Bakiye: Hata';
    });
}
