const usernameField = document.querySelector("#usernameField");
const feedbackField = document.querySelector(".invalid-feedback")
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const EmailfeedbackField = document.querySelector(".emailfeedbackField");
const usernameSuccess = document.querySelector(".usernameSuccess");
const showPassToggle = document.querySelector(".showPassToggle");
const submitBtn = document.querySelector(".submit-btn");


const handleToggleInput= (e)=>{
    if (showPassToggle.textContent === "SHOW"){
        showPassToggle.textContent="HIDE";
        passwordField.setAttribute("type","text");
    }else{
        showPassToggle.textContent="SHOW";
        passwordField.setAttribute("type","Password");
    }
};

showPassToggle.addEventListener("click",handleToggleInput);



emailField.addEventListener("keyup",(e) =>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    EmailfeedbackField.style.display = 'none';

    console.log('emailVal',emailVal);
    if (emailVal.length>0){
        fetch("/authentication/validate-email",{
            body:JSON.stringify({email:emailVal}),
            method: "POST",
        })
        .then(res=>res.json())
        .then(data=>{
            console.log('data',data);
            if(data.email_error){ 
                submitBtn.disabled=true;
                emailField.classList.add("is-invalid");
                EmailfeedbackField.style.display = 'block';
                EmailfeedbackField.innerHTML=`<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }


});


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccess.textContent= `Checking ${usernameVal}`;
    usernameField.classList.remove("is-invalid");
    feedbackField.style.display = 'none';

    console.log('usernameVal',usernameVal);
    if (usernameVal.length>0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({usernameVal:usernameVal}),
            method: "POST",
        })
        .then(res=>res.json())
        .then(data=>{
            usernameSuccess.style.display="none";
            if(data.username_error){ 
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = 'block';
                feedbackField.innerHTML=`<p>${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
        
}); 