var filepath1 = "";
var filepath2 ="";
var filepath3 ="";

async function getfilepath1() {
    // var data = document.getElementById("fileToUpload").value

    var dosya_path = await eel.btn_ResimyoluClick()();
        if (dosya_path) {
            console.log(dosya_path);
            eel.dummy(dosya_path)(function(ret){document.getElementById("file-upload-filename1").innerHTML = "selected featured image: " + ret})
        }
        // document.getElementById("filename_display").value=dosya_path;
        filepath1 = dosya_path
        // infoArea.textContent = 'File name: ' + filepath;
        // document.getElementById("upload_text").value=dosya_path;
        // 
    return dosya_path
    // var data = document.getElementById("fileToUpload").files[0].name;
    // console.log(data)
    
}
async function getfilepath2() {
    // var data = document.getElementById("fileToUpload").value

    var dosya_path = await eel.btn_ResimyoluClick()();
        if (dosya_path) {
            console.log(dosya_path);
            eel.dummy(dosya_path)(function(ret){document.getElementById("file-upload-filename2").innerHTML = "selected image: " + ret})
        }
        // document.getElementById("filename_display").value=dosya_path;
        filepath2 = dosya_path
        // infoArea.textContent = 'File name: ' + filepath;
        // document.getElementById("upload_text").value=dosya_path;
        // 
    return dosya_path
    // var data = document.getElementById("fileToUpload").files[0].name;
    // console.log(data)
    
}
async function getfilepath3() {
    // var data = document.getElementById("fileToUpload").value

    var dosya_path = await eel.btn_ResimyoluClick()();
        if (dosya_path) {
            console.log(dosya_path);
            eel.dummy(dosya_path)(function(ret){document.getElementById("file-upload-filename3").innerHTML = "selected image: " + ret})
        }
        // document.getElementById("filename_display").value=dosya_path;
        filepath3 = dosya_path
        // infoArea.textContent = 'File name: ' + filepath;
        // document.getElementById("upload_text").value=dosya_path;
        // 
    return dosya_path
    // var data = document.getElementById("fileToUpload").files[0].name;
    // console.log(data)
    
}


async function ExtractNews(){
	console.log("running js");
	//turn notification off
	document.getElementById("not_posted").style.visibility ='visible';
	document.getElementById("posted").style.visibility = 'hidden';
	document.getElementById("error").style.visibility = 'hidden';
	document.getElementById("error").innerHTML = "An error occured, please try again";
	
	//get credentials
	var Wordpress_url = document.getElementById('wordpress-add').value
	var Wordpress_username = document.getElementById('username').value
	var Wordpress_password = document.getElementById('password').value
	
	//get language
	var lang = document.getElementById('lang').value
	
	//get pictures
	var picture = document.getElementById('picture_add');
	var opt2 = picture.value;
	var picture_id = 0;
	var p1 = null;
	var p2 = null;
	var p3 = null; 
	
	switch(opt2)
	{
		case "upload":
			picture_id = 1;
			p1 = filepath1;
			p2 = filepath2;
			p3 = filepath3;
			break;
		case "address":
			picture_id = 2;
			p1 = document.getElementById('url_pic1').value;
			p2 = document.getElementById('url_pic2').value;
			p3 = document.getElementById('url_pic3').value;
			break;
		case "nothing":
			picture_id = 0;
			p1 = null;
			p2 = null;
			p3 = null;
	}
	
	//lastly, get content
	var news = document.getElementById('news_extraction');
	var opt3 = news.value;
	var url = null;
	var title = null;
	var content = null;
	var result = false;
	
	switch(opt3)
	{
		case"url":
			url = document.getElementById('url_add').value;
			try{
				await eel.Extract_News(url, lang, picture_id, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password)(function(ret){result = ret; 
				if(result == true){
					document.getElementById("not_posted").style.visibility ='hidden';
					document.getElementById("posted").style.visibility = 'visible';
				}
				else{
					document.getElementById("error").style.visibility = 'visible';
				}});				
			}
			catch(Exception e){
				document.getElementById("error").style.visibility = 'visible';
				document.getElementById("error").innerHTML = "An error occured: " + e;
			}
			break;
		case"manual":
			url = "self";
			title = document.getElementById('title').value;
			content = document.getElementById('content').value;
			
			try{
				await eel.Translating_post(url, content, title, title, p1,p2,p3, lang, picture_id, Wordpress_url, Wordpress_username, Wordpress_password)(function(ret){result = ret;
				if(result == true){
					document.getElementById("not_posted").style.visibility ='hidden';
					document.getElementById("posted").style.visibility = 'visible';
				}
				else{
					document.getElementById("error").style.visibility = 'visible';
				}});				
			}
			catch(Exception e){
				document.getElementById("error").style.visibility = 'visible';
				document.getElementById("error").innerHTML = "An error occured: " + e;
			}
	}
}