var data = '{{ data|tojson }}';
data = data.replace(/\s/g, '');
data = data.replace(/\\/g, '/');
data = JSON.parse(data);
let btn_knn = document.getElementsByClassName("btn_knn");
let btn_select = document.getElementsByClassName("btn_select");
let hoverImg = document.getElementsByClassName("hoverImg");
// console.log("data: " + JSON.stringify(data))
function add_paging() {
    console.log(data['num_page']);
    var url = new URL(window.location.href);
    var cur_index = parseInt(url.searchParams.get("index"));
    var imgpath = url.searchParams.get("imgpath");
    // var labelpath = url.searchParams.get("labelpath");
    if (cur_index == 'undefined') {
        cur_index = 0;
    }
    var i = cur_index - 4;
    if (i > 0) {
        var iDiv = document.createElement('div');
        iDiv.className = 'page_num';
        iDiv.innerHTML = "...";
        document.getElementById("div_page").appendChild(iDiv);
    }
    for (i; ((i < data['num_page']) && (i < cur_index + 4)); i++) {
        if (i < 0) {
            i = 0;
        }
        var iDiv = document.createElement('div');
        iDiv.className = 'page_num';
        var iA = document.createElement('a');
        // iA.href = "?index="+i.toString()+"&imgpath="+imgpath+"&labelpath="+labelpath;
        iA.href = "?index=" + i.toString() + "&imgpath=" + imgpath;
        iA.innerHTML = i.toString();
        if (i == cur_index) {
            iA.style.color = "green";
        }
        iDiv.appendChild(iA);
        document.getElementById("div_page").appendChild(iDiv);
    }
    if (i < data['num_page']) {
        var iDiv = document.createElement('div');
        iDiv.className = 'page_num';
        iDiv.innerHTML = "...";
        document.getElementById("div_page").appendChild(iDiv);
    }
    document.getElementById("div_total_page").innerHTML = "Total: " + data['num_page'].toString() + " page";
}

function add_img(div_id_image) {
    let div_img = document.getElementById("div_img");
    let pagefile_list = data['pagefile'];

    pagefile_list.forEach((item, index) => {
        // console.log('item: ' + JSON.stringify(item))
        $("#div_img").append(
            `<div class= "container_img_btn"  onmouseover="mouseOver(${index})" onmouseout="mouseOut(${index})">
                        <button class="btn_knn" onClick="go_img_search(${item.id})">IR</button>
                        <button class="btn_select" onClick="writecsv(${index},'${item.id},${item.imgpath}')">SELECT</button>
                        <img class="hoverImg" onclick="show_list_segment(${item.id})" src="get_img?fpath=${item.imgpath}">
                        
                    </div>`
        )
    });
}

function mouseOver(id) {
    // console.log('type: ' + typeof(btn_knn))
    btn_knn[id].style.display = "block";
    btn_select[id].style.display = "block";
}

function mouseOut(id) {
    // console.log('type: ' + typeof(btn_knn))
    btn_knn[id].style.display = "none";
    btn_select[id].style.display = "none";
}

function go_img_search(id) {
    window.open("/imgsearch?imgid=" + id);
}

function on_load() {
    var url = new URL(window.location.href);
    var imgpath = url.searchParams.get("imgpath");
    // var labelpath = url.searchParams.get("labelpath");
    // document.getElementById('imgpath').value = imgpath;
    // document.getElementById('labelpath').value = labelpath;
    if ("query" in data) {
        document.getElementById("text_query").value = data["query"]
    }
    add_paging();
    add_img("div_img");
}

function show_list_segment(id) {
    window.open("/showsegment?imgid=" + id);
}

function writecsv(id, info_key) {
    hoverImg[id].style.border = "4px solid red";

    console.log("info_key: " + info_key);
    var mode_write_csv = document.getElementById("mode_write_csv").value;
    console.log("mode_write_csv: " + mode_write_csv);
    var info = {};
    $.ajax({
        url: "writecsv?info_key=" + info_key + "&mode=" + mode_write_csv,
        type: 'GET',
        async: false,
        dataType: 'json',
        success: function(res) {
            console.log("res: ", res);
            info = res;
        }
    });

    str_fname = info["str_fname"]
    console.log("str_fname: " + str_fname);
    number_line = info["number_line"]
    my_alert = str_fname + ' ### number csv line: ' + number_line

    // hoverImg[id].style.border="4px solid red";

    alert("write list shot: " + my_alert);
}

function visualize() {
    var number_of_query = document.getElementById('number_of_query').value;
    console.log("number_of_query: " + number_of_query);
    window.location.href = "visualize?number_of_query=" + number_of_query;
}

function search_image_path() {
    frame_path = document.getElementById('search_image_path').value;

    window.open("/search_image_path?frame_path=" + frame_path)

}

function search() {
    text_query = document.getElementById('text_query').value;

    window.location.href = "/textsearch?textquery=" + text_query;

    document.getElementById('text_query').innerHTML = text_query;
}

function search_asr() {
    text_asr = document.getElementById('text_asr').value;

    window.open("/asrsearch?text_asr=" + text_asr);
}

function ocr_filter() {
    ocr_query = document.getElementById('ocr_filter').value;
    console.log(ocr_query);
    window.open("/ocrfilter?text_ocr=" + ocr_query);
}

function sequence_search() {
    text_query = document.getElementById('text_query').value;
    seq_query = document.getElementById('sequence_search').value;
    console.log(seq_query);
    window.open("/sequencesearch?text_start=" + text_query + '&text_nextframes=' + seq_query);
}

function reset() {
    alert("Clean file submit.csv");
    window.location.href = "http://0.0.0.0:5001/thumbnailimg?index=0";
    // window.location.href = "http://127.0.0.1:5001/thumbnailimg?index=0"
}

function download_btn() {
    // window.location.href = "dowload_submit_file?filename=submit.csv"
    $.ajax({
        type: "GET",
        url: "get_first_row",
        dataType: "json",
        success: function(data) {
            if (data["video_id"] != "None") {
                $.ajax({
                    url: "https://eventretrieval.one/api/v1/submit?item=" + data.video_id + "&frame=" + data.frame_id + "&session=node0a0yuwswfadu2mjgfwcpzqzo744",
                    type: "GET",
                    dataType: "json",
                    success: function(result) {
                        alert(result.description);
                    },
                    error: function(error) {
                        var status = error.status;
                        if (status == 412) {
                            alert("Duplicate or Wrong Format");
                        } else if (status == 401) {
                            alert("Unauthorized Error");
                        }
                    }
                });
            } else {
                alert("Video None")
            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert("Status: " + xhr.status + "     Error: " + thrownError);
        }
    });
}
