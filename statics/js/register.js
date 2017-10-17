function checkname() {
	var check = false;
	var username = document.getElementById("username").value;
	if (username.length > 15) {
		document.getElementById("checkUsername").innerHTML = "  × 不要多于15位";
		check = false;
	}
	else if (username.length <= 0) {
		document.getElementById("checkUsername").innerHTML = "  × 用户名不能为空";
		check = false;
	}
	else {
		document.getElementById("checkUsername").innerHTML = "  √";
		check = true;
	}
	var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
	regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
	if(regEn.test(username) || regCn.test(username)) {
		document.getElementById("checkUsername").innerHTML = "名称不能包含特殊字符";
		check = false;
	}
	return check;
}

function checkpsw() {
	var check = false;
	var password = document.getElementById("password").value;
	if (password.length < 6) {
		document.getElementById("checkPassword").innerHTML = "  × 密码长度不要少于6位";
		check = false;
	} else {
		document.getElementById("checkPassword").innerHTML = "  √";
		check = true;
	}
	var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
		regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
	if(regEn.test(password) || regCn.test(password)) {
		document.getElementById("checkPassword").innerHTML = "密码不能包含特殊字符";
		check = false;
	}
	return check;
}

function checkpsw2() {
	var check = false;
	var password1 = document.getElementById("password").value;
	var password2 = document.getElementById("password2").value;
	if (password1 != password2) {
		document.getElementById("checkPassword2").innerHTML = "  × 两次输入密码不一致";
		check = false;
	} else {
		document.getElementById("checkPassword2").innerHTML = "  √";
		check = true;
	}
	return check;
}

function checkbox() {
	var check = false
	if (!document.getElementsByName("checkbox")[0].checked) {
		document.getElementById("checkCheckbox").innerHTML = "  × 同意我们的条款才可以继续";
		check = false;
	} else {
		document.getElementById("checkCheckbox").innerHTML = "";
		check = true;
	}
	return check;
}

function checkmail() {
	var check = false;
	var usermail = document.getElementById("mail").value;
	var reMail = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,5}$/;
	if (usermail.length <= 0) {
		document.getElementById("checkMail").innerHTML = "  × 邮箱不能为空";
		check = false;
	} 
	else if (!reMail.test(usermail)) {
		document.getElementById("checkMail").innerHTML = "  × 邮箱格式不正确";
		check = false;
	}
	else{
		document.getElementById("checkMail").innerHTML = "  √";
		check = true;
	}

	return check;
}

function check() {
	var check = checkname() && checkpsw() && checkpsw2() && checkbox() && checkmail();
	return check;
}

function isok() {
	confirm("你确定提交吗？")
}

function tishi(){
	alert("欢迎注册")
}

function tishi1(){
	alert("用户存在，无需注册！\n现在登录？\n")
	window.location.href="/login";
}

function tishi2(){
	alert("注册成功！\n现在登录？\n")
	window.location.href="/login";
}