//peader main 文件

function _resize(){
	var size = get_client_size();
    if (size[0] < 1000)
    	size[0] = 1000;
    if(size[1] < 700) 
    	size[1] = 800;
     
     document.getElementById("content-nav").style.height=(size[1]-102)+"px";
     //document.getElementById("content-viewer").style.height=(size[1]-102)+"px";
     document.getElementById("viewer-body").style.height=(size[1]-200)+"px";
     document.getElementById("content-viewer").style.width=(size[0] - 236)+"px";
}
            
        
function get_client_size(){
	if(document.documentElement.clientWidth){
                return [document.documentElement.clientWidth, document.documentElement.clientHeight];
            }else{
                return [document.body.clientWidth, document.body.clientHeight];
            }
}

function sub_scetion_overflow_action  (){
            
            var $sub_section = $('#sub-section');
                            
            $sub_section.mouseenter(function() {
               
                 console.log($sub_section.height());
                 if($sub_section.height() < 210){
                         $sub_section.css('overflow-y','hidden');
                 } else {
                          $sub_section.css('overflow-y','scroll');
                 }
            }).mouseleave(function(){
                    $sub_section.css('overflow-y','hidden');
           });
                      
}

function load_group_menu(){
	 $.ajax({
		type:"GET",
		url:"group",              
		dataType: 'json',
		success:function(groups){                      
			load_groups(groups);
            load_group_click_envent ()                      
       		}
       });
}

function load_groups(groups){
	//var groups = JSON.parse(data);
			var groups_div = '';
			var site_group = null;
			var group;
			for(var i = 0; i < groups.length; i++) {
				group = groups[i];
				if(site_group != group.site_group || i == 0){
					groups_div += '<li class="sub-group"><div class="group-tab"><div class="sub-group-icon"></div><div class="group-name">';
					if(group.site_group == null){
						groups_div += '未分类' ;
                    } else{
                    	groups_div +=  group.site_group ;
                    }     
                    groups_div += '</div></div><ul class="item">';
                    site_group = group.site_group;
                }  
                groups_div = groups_div  + '<li><a href="/#feed/'+  encodeURIComponent(group.site_url) +'"><div class="item-icon"></div><div class="item-name">' 
                            + group.name +'</div><div class="entry-count">(' + group.entry_count + ')</div> </a></li>';
                if( (i+1 < groups.length) && site_group != groups[i+1].site_group){
                	groups_div += '</ul>';
                }
           	}
            groups_div += '</ul></li>';
            $('#group-tree').html(groups_div);  
}

function load_group_click_envent () {
            $( '#group-tree > li > ul')
            .hide()
            .click(function( e ){
                    e.stopPropagation();
            });
                   
            $('#group-tree > li').toggle(
            	function(){
                     $(this).find('ul').slideDown();
                     $(this).find('.sub-group-icon')
                     .css('background-image', 'url("static/images/folder-active.png")');
                }, 
                function(){
                    $( this ).find('ul').slideUp();
                    $(this).find('.sub-group-icon')
                    .css('background-image', 'url("static/images/folder-gray.png")');
           		}
           );   
  
} 

function load_entry_controll () {
	$( '.entry > .entry-body' )
            .click(function( e ){
                    e.stopPropagation();
             })
      .filter(':not(:first)')
      .hide();
             
    $(".entry").live("click", function (){
           var self =  $(this).find('.entry-body').is(':visible');
           if(!self){
               $(this).parent()
               	    .find('.entry-body:visible')
                    .slideToggle();
                }
                
                $(this).find('.entry-body')
                .stop()
                .slideToggle();
                
            });   
}
      
        
        
