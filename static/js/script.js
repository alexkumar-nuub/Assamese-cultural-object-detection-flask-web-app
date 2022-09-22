const api_url = "/api/pred/";

const fileTypes = ["image/png", "image/jpeg"];

var selectedFile;

function checkImage() {

    selectedFile = document.getElementById('file').files[0];
    if (fileTypes.includes(selectedFile.type)) {
        if(selectedFile.size > 10240){
            apiReq(null, selectedFile);
        } else {
            alert("File size too small!!");
        }
    } else {
        alert("Please upload a valid image!!");
    }
}

function apiReq(img_url, file) {
    xhr = new XMLHttpRequest();
    xhr.open("POST", api_url, true);

    const formData = new FormData();
    if (img_url != null) {
        formData.append("url", img_url);
        formData.append("isUrl", "True");
    }
    if (file != null) {
        formData.append("file", file);
        formData.append("isUrl", "False");
    }
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var data = JSON.parse(this.response)

            let imageElement = document.createElement('img');
            imageElement.setAttribute('id', 'image');
            imageElement.setAttribute('src', data.capResult + "?" + new Date().getTime());
            imageElement.setAttribute('alt', 'Input Image');

            if (document.getElementById('form') != null){
                document.getElementById('form').remove();
            }

            if (document.getElementsByClassName('image-view')[0] == null){
                document.getElementsByClassName('box')[0].innerHTML = "<div class='image-view'> </div>";
                document.getElementsByClassName('box')[0].style.display="block";
            }

            // if (file != null) {
            //     getImgData();
            // }

            if (document.getElementsByClassName('home-link')[0] == null){
                var homeLinkDiv = document.createElement('div');
                homeLinkDiv.className = "home-link";
                homeLinkDiv.innerHTML = "<button class='submit-btn'><a href='/'>Home</a></button>";
                document.getElementsByClassName('box')[0].appendChild(homeLinkDiv);
                document.getElementsByClassName('submit-btn')[0].style.marginLeft="unset";
            }

            let myImageDiv = document.getElementsByClassName('image-view')[0];
            myImageDiv.appendChild(imageElement)

        }
    };
    xhr.send(formData);

};

function getImgData() {
    var imgCanvas = document.getElementById("image");
    if (selectedFile) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(selectedFile);
        fileReader.addEventListener("load", function () {
            console.log(imgCanvas);
            console.log(this.result);
            imgCanvas.src = this.result;
        });
    }
}