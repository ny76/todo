
var main = null;

$(document).ready(function() {
  
  main = $('#main');
  
  /*______________________________________________________________
  
          HOME
  */
  
  bind_view('home', null, function(data){
    var html = 'Tasks:<br><br>';
    var list = "<ul id='tasks' style='list-style-type: none;'>";

    if(true){
    data = $.parseJSON(data);
    $.each(data, function (ind, item)
    {
      //html += '<li>' + (ind + 1) + '. ' + item.task + '</li>';
      var id = item._id.$oid;
      var item_ind = ind + 1;
      /*
      html +=
        "<li item_id='" + id + "'>" +
        "<div style='color: navy;' onclick='javascript:'" +
        "  load_view('edit', {id: '" + id + "'}, function(ok){" +
        "    var html = ((ok == 'True') ? 'Added OK' : 'Not Added!');" +
        
        "    return ok;" +
        "  });'>" + (ind + 1) + '. </div><span>' + item.task + '</span></li>';
        */
      list +=
        "<li id='item" + item_ind + "' item_id='" + id + "'>" +
        "  <div id='cmd_edit" + item_ind + "' class='in'><span>" + item_ind + ". </span><span obj='task'>" + item.task +"</span></div> " +
        "  <div class='in'>(" + item.priority + ")</div> " +
        "  <button id='cmd_del" + item_ind + "'>X</button>" +
        '</li>';
    });
    
    list += '</ul>';
    html += list;
    } else
    // show raw data...
      html = data;
    
    set_main(html);

   /*______________________________________________________________
  
          BUILD ITEMS
  */
         
    $('#tasks').find('li').each(function(ind, item){
      item = $(item);
      item_ind = ind + 1;
      var htm_id = item.attr('id');
      var id = item.attr('item_id');
      var edit_item = $('#cmd_edit' + item_ind);
      var del_item = $('#cmd_del' + item_ind);
      var task = item.find("span[obj='task']").text();
//alert(task);      
//alert($('#cmd_edit' + item_ind).attr('id'));
//alert(edit_item.attr('id'));
  /*______________________________________________________________
  
          EDIT
  */

      bind_obj_view(edit_item.attr('id'), 'edit', { id: id }, function(data){
        data = $.parseJSON(data);
        //w(JSON.stringify(data))
        
        var db_task = data.task;
        
        var html = '' +
          "<div id='win'>" +
          "    <div style='vertical-align: middle;'>task: " +
          "    <input id='task' class='inp' value='" + to_html(data.task) + "' /></div>" +
          "    <div style='vertical-align: middle;'>priority: 1" +
          "    <input id='priority' type='range' class='inp' min='1' max='5' defaultValue='1' value='" + to_html(data.priority) + "' />5</div>" +
          "</div>" +
          "<br><br>" +
          "<button id='cmd_save'>UPDATE</button> " +
          "<button id='cmd_del'>DELETE</button> " +
          "<span id='wait' class='nodis'>waiting...</span>";
          
        
        set_main(html);
 
        var act_but = $('#cmd_save');
        var del_but = $('#cmd_del');
        var wait = $('#wait');
        var task = $('#task');
        var priority = $('#priority');
        
        act_but.click(function() {
          act_but.hide();
          del_but.hide();
          wait.show();
          
          send('put', {
            id: id,
            task: task.val(),
            priority: parseInt(priority.val())
          }, function(ok){
            set_main((ok == 'True') ? 'Updated OK' : 'Not Updated!');
          });
        });

        bind_del(del_but, id, db_task);
                  
      }); // bind edit item

      
      bind_del(del_item, id, task);
 
    }); // li items
  });
  
  /*______________________________________________________________
  
          ADD
  */
    
  bind_static_view('add', function() {
    var act_but = $('#cmd_add');
    var wait = $('#wait');
    var task = $('#task');
    var priority = $('#priority');
     
    act_but.click(function() {
      act_but.hide();
      wait.show();
      
      post({
        task: task.val(),
        priority: parseInt(priority.val())
      }, function(ok){
        set_main((ok == 'True') ? 'Added OK' : 'Not Added!');
      }); 
    });  
  });
    
    
  /*
   *
   *
   */

  bind_cmd('dev');
  
  bind_cmd('shutdown');
  
});

  /*______________________________________________________________
  
          HELPER FUNCS
  */

  
function bind_del(obj, id, task) {
  /*______________________________________________________________
  
          DELETE
  */
  obj.click(function() {
    var html = '' +
      "<div id='win'>" +
      "    <span style='display: inline-block; vertical-align: middle;'>task: " + task + "</span>" +
      "</div>" +
      "<br><br>" +
      "<button id='cmd_del'>DELETE</button>" +
      "<button id='cmd_canc'>CANCEL</button>" +
      "<span id='wait' class='nodis'>waiting...</span>";

    set_main(html);

    act_but = $('#cmd_del');
    canc_but = $('#cmd_canc');
    wait = $('#wait');

    bind_cmd_send('del', 'delete', {id: id}, function(ok){
      set_main((ok == 'True') ? 'Deleted OK' : 'Not Deleted!');
    });
    
    bind_main(canc_but);
  });
}
 
function set_main(str) {
  //w('set main(' + str + ')');
  $('#main').html((str) ? str : '');
}

function bind_cmd(cmd, data, on_complete) {
  $('#cmd_' + cmd).click(function() {
    $.get('/' + cmd, data, ((on_complete) ? on_complete : set_main));
  }); 
}

function bind_static_view(view, on_load) {
  $('#show_' + view).click(function() { load_static_view(view, on_load); });
}

function load_static_view(view, on_load) {
  main.load('/static/htm/' + view + '.html', null, on_load);
}

function bind_view(view, data, data_handler) {
  $('#show_' + view).click(function() { load_view(view, data, data_handler); });
}

function load_view(view, data, data_handler) {
  var all_data = ((data) ? data : {});
  
  all_data.view = view;
  
  $.get('/data', all_data, data_handler);
}

function bind_obj_view(obj, view, data, data_handler) {
    var all_data = ((data) ? data : {});
  
    all_data.view = view;

  $('#' + obj).click(function() {
    $.get('/data', all_data, get_handler(data_handler));
    /*
    $.ajax({
      method: 'get',
      url: '/data',
      data: all_data,
      complete: ((data_handler) ? data_handler : set_main)
    });*/
  });
}

function bind_cmd_view(cmd, view, data, data_handler) {
  var all_data = ((data) ? data : {});
  
  all_data.view = view;

  $('#cmd_' + cmd).click(function() {
    $.get('/data', all_data, get_handler(data_handler));
  });
}

function post(data, data_handler) {
  var all_data = { data: JSON.stringify(data) };
 
  $.post('/data', all_data, get_handler(data_handler));
}

function bind_cmd_send(cmd, method, data, data_handler) {
  $('#cmd_' + cmd).click(function() {
    send(method, data, data_handler);
  });
}

function send(method, data, data_handler) {
  var all_data = {};
  var url='/data';
  var data_type = 'json';

  if(method != 'delete') {
    all_data.data = JSON.stringify(data);
    //all_data = data;
  } else {
    method = 'get';
    url = '/delete';
    all_data = data;
    data_type = 'text';
  }
   //alert(JSON.stringify(all_data));
   
  $.ajax({
    method: method,
    url: url,
    data: all_data,
    dataType: data_type,
    complete: get_handler(data_handler)
    //complete: function(data) { w(JSON.stringify(data)); }
  });
}

function bind_main(obj) {
  obj.click(function() {
    set_main('');
  });
}

function get_handler(data_handler) {
  return function(data) {
      if(data.responseText)
        data = data.responseText;

      ((data_handler) ? data_handler : set_main)(data);
  };
}


function w(obj) {
  $('#DEV').text((obj) ? obj.toString() : 'NULL');
}

function to_html(str) {
  return String(str).replace('\'', '&#39;');
}

function disable(container, id) {
  var el = container.getElementById(id);
  
  if(el) el.disabled = true; 
}

function show(container, id) {
  var el = container.getElementById(id);
  
  if(el) el.style.display = ''; 
}

function show_by_name(container, name) {
  var els = container.getElementsByName(name);
  
  if(els) els[0].style.display = ''; 
}

function hide(container, id) {
  var el = container.getElementById(id);
  
  if(el) el.style.display = 'none'; 
}

function hide_by_name(container, name) {
  var els = container.getElementsByName(name);
  
  if(els) els[0].style.display = 'none'; 
}




