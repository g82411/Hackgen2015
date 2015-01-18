var person_id = "";
var now_group = "";

function create_group_callback( json ) {
  group_arr = json["groupList"];
  $("#group-field").html("");
  for(var i in group_arr) {
    groupname = group_arr[i]["groupName"];
    groupid = group_arr[i]["groupID"];
    $("#group-field").append("<a href=\"#group-index\" id=\"group_"+groupid+"\" class=\"group-label ui-link ui-btn ui-shadow ui-corner-all\" data-role=\"button\" role=\"button\">"+groupname+"</a>")
  }
}

function add_user_callback( json ) {
  $("#user-name").html(json["userName"]);
  var storage = window.localStorage;
  window.localStorage.setItem("person_id", json["userID"]);
  person_id = json["userID"];
}

function view_group_callback( json ) {
  create_group_callback( json );
}

function update_userName_callback( json ) {
  $("#user-name").html(json["userName"]);
}

function parseUserID_callback( json ) {
  update_userName_callback( json );
}

function search_group_callback( json ) {
  $("#group-info").html("");
  $("#group-info").append("群組名稱："+json["groupName"]+"</br>");
  $("#group-info").append("群組創建人："+json["owner"]+"</br>");
  $("#group-info").append("結算時間："+json["groupPushTime"]+"</br>");
  $("#group-info").append("結算星期：</br>");
  if(json["sun"]) {
    $("#group-info").append("Sun ");
  }
  if(json["mon"]) {
    $("#group-info").append("Mon ");
  }
  if(json["tue"]) {
    $("#group-info").append("Tue ");
  }
  if(json["wed"]) {
    $("#group-info").append("Wed ");
  }
  if(json["thu"]) {
    $("#group-info").append("Thu ");
  }
  if(json["fri"]) {
    $("#group-info").append("Fri ");
  }
  if(json["sat"]) {
    $("#group-info").append("Sat ");
  }
  $("#group-info").append("</br>");
  $("#group-info").append("預設吃吃："+json["defaultValue"]+"</br>");
  if(json["isJoin"]) {
    $("#group-info").append("<a href=\"#\" class=\"ui-link ui-btn ui-shadow ui-corner-all\" data-role=\"button\" role=\"button\">您已經加入</a>");
  }
  else {
    $("#group-info").append("<a href=\"#index\" class=\"join-group ui-link ui-btn ui-shadow ui-corner-all\" data-role=\"button\" role=\"button\" id=\"group_add_"+json["groupID"]+"\">加入群組</a>");
  }
}

function join_callback( json ) {
  create_group_callback( json );
}

function add_choose_callback( json ) {
  var chooseList = json["chooseList"];
  $("#group-choice").html("");
  $("#group-choice").append('<fieldset id="choose_content" data-role="controlgroup">')
  for(var i in chooseList) {
    var voteNum = chooseList[i]["voteNumber"];
    var choose_id = chooseList[i]["id"];
    var choose_name = chooseList[i]["name"];
    $("#choose_content").append('\
      <fieldset class="ui-grid-a">\
        <div class="ui-block-a">\
          <input type="radio" name="group-choice" id="choose_'+choose_id+'"value="choose_'+choose_id+'">\
          <label for="choose_'+choose_id+'">'+choose_name+'</label>\
        </div>\
        <div class="ui-block-b">\
          <a href="#group-member" id="choose_vote_num_'+choose_id+'" class="choose_vote_num ui-btn ui-icon-user ui-btn-icon-left">'+voteNum+'</a>\
        </div>\
      </fieldset>\
    ')
  }
}

function view_choose_callback( json ) {
  add_choose_callback( json );
}

function view_member_callback( json ) {
  add_choose_callback( json );
}

function view_vote_member( json ) {
  add_choose_callback( json );
}

function getGroup() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/viewGroup?callback=?",
    dataType:"jsonp",
    data: {userID: person_id}
  })
}

function getName() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/parseUserID?callback=?",
    dataType:"jsonp",
    data: {userID: person_id}
  }).done({

  })
}

$(function() {
  setTimeout(function() {
    var storage = window.localStorage;
    person_id = window.localStorage.getItem("person_id");
    if(!person_id) {
      $( "#add-user" ).popup();
      $( "#add-user" ).popup("open");
    }
    else {
      getGroup();
      getName();
    }
  }, 100);
})

$(function() {
  $("#add-user-submit").click(function() {
    $.ajax({
      type: "GET",
      url: "http://128.199.152.153:8000/addUser?callback=?",
      dataType:"jsonp",
      data: {username: $("#add-user-value").val()}
    }).done({

    })
  })
})

$(function() {
  $("#change-username-submit").click(function() {
    $.ajax({
      type: "GET",
      url: "http://128.199.152.153:8000/updateUserName?callback=?",
      dataType:"jsonp",
      data: {userID: person_id, userName: $("#change-username-value").val()}
    })
    $("#change-username-value").val("");
  })
})

$(".group-label").live('click', function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/viewChoose?callback=?",
    dataType:"jsonp",
    data: {userID: person_id, groupID: $(this).attr("id").substring(6)}
  })
  now_group = $(this).attr("id").substring(6);
})

$("#search-group").live('keypress', function (e) {
  if(event.which==13) {
    event.preventDefault();
    $.ajax({
      type: "GET",
      url: "http://128.199.152.153:8000/searchGroup?callback=?",
      dataType:"jsonp",
      data: {groupID: $(this).val(), userID: person_id}
    })
  }
})

$(".ui-input-clear").live("click", function() {
  $("#group-info").html("");
})

$(".join-group").live("click", function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/join?callback=?",
    dataType:"jsonp",
    data: {userID: person_id, groupID: $(this).attr("id").substring(10)}
  })
  $("#group-info").html("");
  $("#search-group").val("");
})

$("#add-choice-submit").live("click", function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/addChoose?callback=?",
    dataType:"jsonp",
    data: {userID: person_id, groupID: now_group, chooseName: $("#add-choose-value").val()}
  })
  $("#add-choose-value").val("");
})

$("#view_member").live("click", function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/viewMember?callback=?",
    dataType:"jsonp",
    data: {groupID: now_group}
  })
})

$(".choose_vote_num").live("click", function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/viewVoteMember?callback=?",
    dataType:"jsonp",
    data: {groupID: now_group, chooseID: $(this).attr("id").substring(16)}
  })
})

$(function() {
  $("#create-group-submit").click(function() {
    var groupname = $("#group-name").val();
    var timeset = $("#time-set").val();
    if($("#day-set-sun").attr("data-cacheval") == "false") {
      var daysetsun = true;
    }
    else {
      var daysetsun = false;
    }
    if($("#day-set-mon").attr("data-cacheval") == "false") {
      var daysetmon = true;
    }
    else {
      var daysetmon = false;
    }
    if($("#day-set-tue").attr("data-cacheval") == "false") {
      var daysettue = true;
    }
    else {
      var daysettue = false;
    }
    if($("#day-set-wed").attr("data-cacheval") == "false") {
      var daysetwed = true;
    }
    else {
      var daysetwed = false;
    }
    if($("#day-set-thu").attr("data-cacheval") == "false") {
      var daysetthu = true;
    }
    else {
      var daysetthu = false;
    }
    if($("#day-set-fri").attr("data-cacheval") == "false") {
      var daysetfri = true;
    }
    else {
      var daysetfri = false;
    }
    if($("#day-set-sat").attr("data-cacheval") == "false") {
      var daysetsat = true;
    }
    else {
      var daysetsat = false;
    }
    var defaulttoeat = $("#default-to-eat").val();

    $.ajax({
      type: "GET",
      url: "http://128.199.152.153:8000/addGroup?callback=?",
      dataType:"jsonp",
      data: { groupname: groupname, timeset: timeset, daysetsun: daysetsun, daysetmon: daysetmon, daysettue: daysettue, daysetwed: daysetwed, daysetthu: daysetthu, daysetfri: daysetfri, daysetsat: daysetsat, defaulttoeat: defaulttoeat, userID: person_id }
    })

    $("#group-name").val("");
    $("#time-set").val("");
    $("#default-to-eat").val("");
    $(".day-input").attr("data-cacheval", "true");
    $(".day-label").removeClass("ui-btn-active");
    $(".day-label").removeClass("ui-checkbox-on");
    $(".day-label").addClass("ui-checkbox-off");

  })
})
