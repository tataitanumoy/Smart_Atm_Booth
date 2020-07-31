$("#btnLogin").on("click",function(){
    if(ValidateUserinfo()){
        $("#btnLogin").html("Logging in...");
        $.ajax({
            method: "POST",
            url: "./api/userlogin",
            contentType: "application/json",
            data: JSON.stringify({username: $("#txtUserName").val().trim(), password: $("#txtPassword").val().trim()})
          })
          .done(function(data) {
            $("#btnLogin").html("Log In");
            if(data!=null)
            {
                location.href="/dashboard";
            }
            else{
                alert("Invalid user information provided.")
            }
            
          });
       
    }
})

//Validate user login
function ValidateUserinfo(){
    var IsValid=true;
    if($("#txtUserName").val().trim()==""){
        alert("Enter username");
        IsValid=false;
    }
    else if($("#txtPassword").val().trim()==""){
        alert("Enter passwoird");
        IsValid=false;
    }
    return IsValid
}