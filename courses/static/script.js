const input = document.querySelector('#password');
const icon = document.querySelector('.toggle-pass');
icon.addEventListener('click', () => {
    icon.classList.toggle('bi-eye-slash');
    icon.classList.toggle('bi-eye');
    input.type = (input.type === 'password') ? 'text' : 'password';
});