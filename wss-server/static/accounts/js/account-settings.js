(function () {
	'use strict';
	window.addEventListener('load', function () {
		// Fetch all the forms we want to apply custom Bootstrap validation styles to
		var forms = document.getElementsByClassName('needs-validation');
		// Loop over them and prevent submission
		if (forms)
			var validation = Array.prototype.filter.call(forms, function (form) {
				form.addEventListener('submit', function (event) {
					if (form.checkValidity() === false) {
						event.preventDefault();
						event.stopPropagation();
					}
					form.addClass('was-validated');
				}, false);
			});
	}, false);
})();

if (document.querySelector("#phonenumberInput")) {
    let cleaveBlocks = new Cleave('#phonenumberInput', {
        delimiters: ['(', ')', '-'],
        blocks: [0, 3, 3, 4]
    });
}

$("#change_personal_info_button").click(function() {
    let first_name = $("#firstnameInput").val();
    let last_name = $("#lastnameInput").val();
    let phone = $("#phonenumberInput").val();
    let username = $("#usernameInput").val();

    if (!username){
        $("#usernameEmptyTip").css("display", "block");
        return
    }
    else{
        $("#usernameEmptyTip").css("display", "none");
    }

    $.ajax({
        url:'change_personal_info/',
        type:'post',
        data:{"first_name": first_name, "last_name": last_name, "phone": phone, "username": username},
        success:function (data) {
            Swal.fire({
                title: 'Personal Info Settings',
                text: 'Personal info settings update successfully!',
                icon: "success",
                confirmButtonClass: 'btn btn-primary w-xs mt-2',
                buttonsStyling: false,
                showCloseButton: true
            }).then((isConfirm) => {
                if (isConfirm.value) {
                    window.location.reload();
                }
            });
        }});
});


/* 
    Change password
 */

// Password match
let password = document.getElementById("newpasswordInput"),
    confirm_password = document.getElementById("confirmpasswordInput");

function validatePassword() {
    if (password.value !== confirm_password.value) {
        $("#passwordNotMatchTips").css("display","block");
    } else {
        $("#passwordNotMatchTips").css("display","none");
    }
}

// Password validation
confirm_password.onchange = validatePassword;

let newPasswordInput = document.getElementById("newpasswordInput");
let letter = $("#pass-lower");
let capital = $("#pass-upper");
let number = $("#pass-number");
let length = $("#pass-length");

// When the user starts to type something inside the password field
newPasswordInput.onkeyup = function () {
    // Validate lowercase letters
    let lowerCaseLetters = /[a-z]/g;
    if (newPasswordInput.value.match(lowerCaseLetters)) {
        letter.removeClass("invalid");
        letter.addClass("valid");
    } else {
        letter.removeClass("valid");
        letter.addClass("invalid");
    }

    // Validate capital letters
    let upperCaseLetters = /[A-Z]/g;
    if (newPasswordInput.value.match(upperCaseLetters)) {
        capital.removeClass("invalid");
        capital.addClass("valid");
    } else {
        capital.removeClass("valid");
        capital.addClass("invalid");
    }

    // Validate numbers
    let numbers = /[0-9]/g;
    if (newPasswordInput.value.match(numbers)) {
        number.removeClass("invalid");
        number.addClass("valid");
    } else {
        number.removeClass("valid");
        number.addClass("invalid");
    }

    // Validate length
    if (newPasswordInput.value.length >= 8) {
        length.removeClass("invalid");
        length.addClass("valid");
    } else {
        length.removeClass("valid");
        length.addClass("invalid");
    }
};

let passwordTip = function (tip_obj, is_empty) {
    if (is_empty){
        tip_obj.css("display","block");
    }
    else{
        tip_obj.css("display","none");
    }
    return !is_empty
}

$("#changePasswordButton").click(function() {
    let old_password = $("#oldpasswordInput").val();
    let new_password = $("#newpasswordInput").val();
    let confirm_password = $("#confirmpasswordInput").val();

    passwordTip($("#oldPasswordEmptyTip"), !old_password);
    passwordTip($("#newPasswordEmptyTip"), !new_password);
    passwordTip($("#confirmPasswordEmptyTip"), !confirm_password);

    if (!old_password || !new_password || !confirm_password){return}

    if (!letter.hasClass('valid') || !capital.hasClass('valid') ||
        !number.hasClass('valid') || !length.hasClass('valid')) {return;}

    validatePassword();

    if (new_password === confirm_password) {
        $.ajax({
            url:'change_password/',
            type:'post',
            data:{"old_password": old_password, "new_password": new_password, "confirm_password": confirm_password},
            success:function (data) {
                Swal.fire({
                    title: 'Change Password Success',
                    text: 'Password change successfully!',
                    icon: "success",
                    confirmButtonClass: 'btn btn-primary w-xs mt-2',
                    buttonsStyling: false,
                    showCloseButton: true
                });
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                if (errorThrown === 'Unauthorized'){
                    Swal.fire({
                        title: 'Change Password Failed',
                        text: 'Old password did not match the record',
                        icon: "error",
                        confirmButtonClass: 'btn btn-primary w-xs mt-2',
                        buttonsStyling: false,
                        showCloseButton: true
                    });
                }
            }
        });
    }
});


$(".notification-settings").change(function() {
    let notification_type = $(this).data("notification-type");
    let value = $(this).val();
    $.ajax({
        url:"notification_settings/",
        type:'post',
        data: {"notification_type": notification_type, "value":value},
        success:function (data) {
        }});
});

$("#deleteAccountConfirm").click(function() {
    let confirm_password = $("#deleteAccountPassword").val();

    if (!confirm_password){
        $("#deleteAccountPasswordEmptyTips").css("display", "block");
        return
    }
    else{
        $("#deleteAccountPasswordEmptyTips").css("display", "none");
    }

    $.ajax({
        url:'delete_account/',
        type:'post',
        data:{"confirm_password": confirm_password},
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            if (errorThrown === 'Unauthorized'){
                $("#deleteAccountPasswordNotMatchTips").css("display", "block");
            }
        }
});
});
