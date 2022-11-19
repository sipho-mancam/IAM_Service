
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signUpForm = document.getElementById('sign-up');
const signInForm = document.getElementById('sign-in');

signUpButton.addEventListener('click', () =>{
    signUpForm.style.zIndex = '1';
    signInForm.style.zIndex = '0';
});

signInButton.addEventListener('click', () =>{
    signUpForm.style.zIndex = '0';
    signInForm.style.zIndex = '1';
})