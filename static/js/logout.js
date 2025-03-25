document.getElementById('logoutBtn').addEventListener('click', function() {
    const token = localStorage.getItem('token');
    
    // Çıkış işlemi için GET isteği gönderiyoruz
    fetch('/logout', {
        method: 'GET',  // GET metodu kullanılıyor
        headers: {
            'Authorization': `Bearer ${token}`,  // Token'ı yetkilendirme başlığında gönderiyoruz
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        localStorage.removeItem('token');  // Token'ı yerel depolamadan sil
        //window.location.href = '/login';  // Kullanıcıyı login sayfasına yönlendir
        window.location.href = '/';  // Kullanıcıyı anasayfaya yönlendir
    })
    .catch(error => {
        window.location.href = '/login';
        console.error("Error:", error);
    });
});
