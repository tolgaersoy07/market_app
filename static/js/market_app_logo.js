function createMarketAppLogo() {
    const logoDiv = document.createElement('div');
    logoDiv.classList.add('brand');
    logoDiv.textContent = 'MarketApp';
    const style = document.createElement('style');
    style.textContent = `
        .brand {
            background: #ff7300;
            color: white;
            padding: 15px 30px;
            border-radius: 20px;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style);
    logoDiv.addEventListener('click', () => {
        window.location.href = '/';
    });
    return logoDiv;
}

document.addEventListener('DOMContentLoaded', function () {
    let logoContainer = document.getElementById('logo-container');
    if (!logoContainer) {
        logoContainer = document.createElement('div'); 
        logoContainer.id = 'logo-container';  
        document.body.insertBefore(logoContainer, document.body.firstChild); 
    }
    const marketAppLogo = createMarketAppLogo();
    logoContainer.appendChild(marketAppLogo);
});