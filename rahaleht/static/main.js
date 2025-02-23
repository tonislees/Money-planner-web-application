const menuButton = document.querySelector('li#home-id');
const menuButtonBg = document.querySelector('li#home-id p');
const sidebar = document.querySelector('.sidebar-container');
const content = document.querySelector('.content-container');

sidebar.style.transition = 'none';
content.style.transition = 'none';
menuButton.style.transition = 'none';

if (localStorage.getItem('toggle') === 'true') {
    sidebar.classList.add('sidebar-active');
    menuButton.classList.add('active');
    content.classList.add('content-container-sidebar');
};

setTimeout(() => {
    sidebar.style.transition = '0.6s';
    content.style.transition = '0.6s';
    menuButton.style.transition = '0.6s';
}, 1);

menuButtonBg.addEventListener('click', () => {
    sidebar.classList.toggle('sidebar-active');
    menuButton.classList.toggle('active');
    content.classList.toggle('content-container-sidebar');
    const isActive = sidebar.classList.contains('sidebar-active');
    localStorage.setItem('toggle', isActive ? 'true' : 'false');
});

if (window.location.pathname === '/settings') {
    const profilePicLang = document.getElementById('profile-pic-lang');
    const resetProfilePicLang = document.getElementById('reset-profile-pic-lang');
    const defaultProfilePicLang = document.getElementById('default-profile-pic-lang');
    const fileSelectedLang = document.getElementById('file-selected-lang');
    console.log(profilePicLang.value);
    imageLabel = document.getElementById('file-upload-label');
    document.getElementById('file-upload').addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            imageLabel.classList.add('selected');
            imageLabel.textContent = fileSelectedLang.value;
        }
        else {
            imageLabel.classList.remove('selected');
            imageLabel.textContent = profilePicLang.value;
        }
    });

    defaultPicture = document.getElementById('default-picture-label');
    picsDiv = document.querySelector('.buttons-container');
    document.getElementById('default-picture').addEventListener('change', function() {
        if (this.checked) {
            defaultPicture.classList.add('selected');
            defaultPicture.textContent = defaultProfilePicLang.value;
            imageLabel.style.display = 'none';
            picsDiv.style.justifyContent = 'center';
        } else {
            defaultPicture.classList.remove('selected');
            defaultPicture.textContent = resetProfilePicLang.value;
            imageLabel.style.display = 'block';
            picsDiv.style.justifyContent = 'space-around';
        }
    });
}