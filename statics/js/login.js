function lalala(str) {
	if(str){
		document.getElementById("username").value = '';
		document.getElementById("username").placeholder = str;
	}
	
}

function hahaha(str) {
	if(str){
		document.getElementById("userpsw").value = '';
		document.getElementById("userpsw").placeholder = str;
	}
	
}

function checkName() {
	var check = false;
	var username = document.getElementById("username").value;
	if (username.length > 10) {
		lalala("  × 不要多于10位");
		document.getElementById("checkName_text").innerHTML = "&nbsp;&nbsp;";
		check = false;
	}
	else if (username.length <= 0) {
		lalala("  × 用户名不能为空");
		document.getElementById("checkName_text").innerHTML = "&nbsp;&nbsp;";
		check = false;
	} 
	else {
		document.getElementById("checkName_text").innerHTML = " √";
		check = true;
	}

	var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
		regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
	if(regEn.test(username) || regCn.test(username)) {
		lalala("  × 不能包含特殊字符");
		document.getElementById("checkName_text").innerHTML = "&nbsp;&nbsp;";
		check = false;
	}

	return check;
}

function checkPsw() {
	var check = false;
	var password = document.getElementById("userpsw").value;
	if (password.length < 6) {
		hahaha(" × 不要少于6位")
		document.getElementById("checkPsw_text").innerHTML = "&nbsp;&nbsp;";
		check = false;
	} else {
		document.getElementById("checkPsw_text").innerHTML = " √";
		check = true;
	}

	var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
		regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
	if(regEn.test(password) || regCn.test(password)) {
		lalala(" × 不能包含特殊字符");
		document.getElementById("checkPsw_text").innerHTML = "&nbsp;&nbsp;";
		check = false;
	}

	return check;
}

function check() {
	var check = checkName() && checkPsw();
	return check;
}

