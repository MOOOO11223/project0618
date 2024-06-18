function ShowTime(){
    　	var NowDate=new Date();
        var month=NowDate.getMonth()+1;
        var day=NowDate.getDate();
    　	var h=NowDate.getHours();
    　	var m=NowDate.getMinutes();
        var s=NowDate.getSeconds();　
        document.getElementById('showbox').innerHTML = month+"/"+day+" "+h+':'+m+':'+s;
        setTimeout('ShowTime()',1000);
        }