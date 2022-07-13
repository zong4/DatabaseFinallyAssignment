var session = document.getElementById("session")

if(session.innerText == "Admin")
{
    var addButton = document.querySelectorAll('[id=addButton]');
    for(var i = 0; i < addButton.length; i++) {
        addButton[i].style.display = 'float';
    }

    var updateButton = document.querySelectorAll('[id=updateButton]');
    for(var i = 0; i < updateButton.length; i++) {
        updateButton[i].style.display = 'float';
    }

    var deleteButton = document.querySelectorAll('[id=deleteButton]');
    for(var i = 0; i < deleteButton.length; i++) {
        deleteButton[i].style.display = 'float';
    }
}
else
{
    var addButton = document.querySelectorAll('[id=addButton]');
    for(var i = 0; i < addButton.length; i++) {
        addButton[i].style.display = 'none';
    }

    var updateButton = document.querySelectorAll('[id=updateButton]');
    for(var i = 0; i < updateButton.length; i++) {
        updateButton[i].style.display = 'float';
    }

    var deleteButton = document.querySelectorAll('[id=deleteButton]');
    for(var i = 0; i < deleteButton.length; i++) {
        deleteButton[i].style.display = 'none';
    }
}


var flash = document.getElementById("flash");

if(flash != null)
    if(flash.innerText == "False")
        alert("操作失败");


var form = document.getElementById("form");


var ClickFun = function (e) {
    e = e || window.event;

    if(!form.contains(window.event.target) && form.style.display == "block")
    {
        alert("Please close the form firstly!");
    }
}

window.onmousedown = document.mousedown = ClickFun;