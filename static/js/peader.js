//peader main 文件

var Peader = {
    current_page: 1

};

function _resize() {
    var size = get_client_size();
    if (size[0] < 1000)
        size[0] = 1000;
    if (size[1] < 700)
        size[1] = 800;

    document.getElementById("content-nav").style.height = (size[1] - 102) + "px";
    //document.getElementById("content-viewer").style.height=(size[1]-102)+"px";
    document.getElementById("viewer-body").style.height = (size[1] - 153) + "px";
    document.getElementById("content-viewer").style.width = (size[0] - 236) + "px";
}

function get_client_size() {
    if (document.documentElement.clientWidth) {
        return [document.documentElement.clientWidth, document.documentElement.clientHeight];
    } else {
        return [document.body.clientWidth, document.body.clientHeight];
    }
}

function sub_scetion_overflow_action() {

    var $sub_section = $('#sub-section');

    $sub_section.mouseenter(function () {

        if ($sub_section.height() < 210) {
            $sub_section.css('overflow-y', 'hidden');
        } else {
            $sub_section.css('overflow-y', 'scroll');
        }
    }).mouseleave(function () {
            $sub_section.css('overflow-y', 'hidden');
        });

}

function load_group_menu() {
    $.ajax({
        type: "GET",
        url: "group",
        dataType: 'json',
        success: function (groups) {
            load_groups(groups);
            load_group_click_envent();
            load_feed_link_click_envent();
        }
    });
}

function load_groups(groups) {
    //alert(groups.length)

    //var groups = JSON.parse(data);
    var groups_div = '';
    var site_group = null;
    var group;
    for (var i = 0; i < groups.length; i++) {
        group = groups[i];
        //alert(group)

        if (site_group != group.site_group || i == 0) {
            groups_div += '<li class="sub-group"><div class="group-tab"><div class="sub-group-icon"></div><div class="group-name">';
            if (group.site_group == null) {
                groups_div += '未分类';
            } else {
                groups_div += group.site_group;
            }
            groups_div += '</div></div><ul class="item">';
            site_group = group.site_group;
        }
        groups_div = groups_div + '<li><a href="/#' + encodeURIComponent(group.site_url) + '"><div class="item-icon"></div><div class="item-name">'
            + group.name + '</div><div class="entry-count">(' + group.entry_count + ')</div> </a></li>';
        if ((i + 1 < groups.length) && site_group != groups[i + 1].site_group) {
            groups_div += '</ul>';
        }
    }
    groups_div += '</ul></li>';
    $('#group-tree').html(groups_div);
}

function load_group_click_envent() {
    $('#group-tree > li > ul')
        .hide()
        .click(function (e) {
            e.stopPropagation();
        });
    $('#group-tree > li').toggle(
        function () {
            $(this).find('ul').slideDown();
            $(this).find('.sub-group-icon')
                .css('background-image', 'url("static/images/folder-active.png")');
        },
        function () {
            $(this).find('ul').slideUp();
            $(this).find('.sub-group-icon')
                .css('background-image', 'url("static/images/folder-gray.png")');
        }
    );

}

function load_entry_controll() {

    $(".entry").live("click", function () {

        var self = $(this).find('.entry-body').is(':visible');
        if (!self) {
            $(this).parent()
                .find('.entry-body:visible')
                .slideToggle();
        }
        $(this).find('.entry-body')
            .stop()
            .slideToggle();
        var $entry_abr = $(this).find('.entry-abr');
        if (!$entry_abr.hasClass('entry-read')) {
            $entry_abr.addClass('entry-read');
            var entry_id = $(this).find('.entry-id').text();
            label_entry_read(entry_id);
        }

        $(this).parent().scrollTop($('.entry').index($(this)) * 41);
        return false;
    });


}

var EntryFormator = {
    entry_begin: '<div class="entry">',
    entry_end: '</div>',
    entry_abr: function () {
        var abr_read = "entry-abr";
        var abr_love = "like dislike-icon";
        if (this.entry.read == 1) {
            abr_read = "entry-abr entry-read";
        }
        if (this.entry.love == 1) {
            abr_love = "like like-icon";
        }
        var abr_begin = '<div class="' + abr_read + '"><span class="' + abr_love + '"></span>';

        var entry_id_span = '<span class="entry-id">' + this.entry.entry_id + '</span>';
        var abr_title = '<div class="entry-title">' + this.entry.title.replace(/<[^>]+?>/g, "") + '</div>';
        var abr_end = '</div>';
        return abr_begin + entry_id_span + abr_title + abr_end;
    },
    entry_body: function () {
        var entry_title = '<a href="' + this.entry.link + '" target="_blank" class="entry-link"><h3>' + this.entry.title + '</h3></a>';
        var entry_body_begin = '<div class="entry-body"><div class="entry-content">' + entry_title;

        var entry_body_end = '</div>';

        return entry_body_begin + this.entry.description + entry_body_end;
    },
    format: function (entry) {
        this.entry = entry;
        return this.entry_begin + this.entry_abr() + this.entry_body() + this.entry_end;
    }

};

function ajax_load_entry_page() {
    var site_url = decodeURIComponent(window.location.hash.slice(1));

    $.ajax({
        type: "POST",
        url: "feed",
        data: {'site_url': site_url, 'page': Peader.current_page},
        dataType: 'json',
        success: function (entries) {
            for (var i  in entries) {
                if (i == 0) {
                    $('#viewer-body').html(EntryFormator.format(entries[i]));
                } else {
                    $('#viewer-body').append(EntryFormator.format(entries[i]));
                }
            }

            $(".entry a").attr('target', '_blank');
            $('.entry > .entry-body')
                .click(function (e) {
                    e.stopPropagation();
                })
                .hide();

        }
    });

}

function get_base_url(url) {

    var baseURL = url.substring(0, url.indexOf('/', 14));


    if (baseURL.indexOf('http://localhost') != -1) {
        // Base Url for localhost
        var url = location.href;  // window.location.href;
        var pathname = location.pathname;  // window.location.pathname;
        var index1 = url.indexOf(pathname);
        var index2 = url.indexOf("/", index1 + 1);
        var baseLocalUrl = url.substr(0, index2);

        return baseLocalUrl + "/";
    }
    else {
        // Root Url for domain name
        return baseURL + "/";
    }

}
function load_feed_link_click_envent() {
    $('.item > li').click(function () {
        //detect hash change
        Peader.current_page = 1;
        window.location.hash = $(this).find('a').attr('href').substring(1);
        var site_url = decodeURIComponent(window.location.hash.slice(1)); //hash to string (= "myanchor")
        $('#item-count').html('<h3>' + $(this).find('.item-name').text() + '</h3>');
        ajax_load_entry_page();
        Peader.current_page++;
    });
}

function to_next_page() {
    $("#item-next-button").click(
        function () {
            ajax_load_entry_page();
            Peader.current_page++;
        });
}

function toggle_like() {

    $(".like").live("click",
        function (e) {
            e.stopPropagation();
            var love = 0;
            if ($(this).hasClass('dislike-icon')) {
                $(this).removeClass('dislike-icon');
                $(this).addClass('like-icon');
                love = 1;

            } else {
                $(this).removeClass('like-icon');
                $(this).addClass('dislike-icon');
            }
            var entry_id = $(this).parent().find('.entry-id').text();
            toggle_entry_love(entry_id, love);
            return false;
        });
}


function label_entry_read(entry_id) {
    $.ajax({
        type: "GET",
        url: "entry/read",
        data: {'entry_id': entry_id},
        dataType: 'text',
        success: function (msg) {
            if (msg == "ok") {
                return ture;
            }
        }
    });
}


function toggle_entry_love(entry_id, love) {
    $.ajax({
        type: "GET",
        url: "entry/love",
        data: {'entry_id': entry_id, 'love': love},
        dataType: 'text',
        success: function (msg) {
            if (msg == "ok") {
                return ture;
            }
        }
    });
}




      
        
        
