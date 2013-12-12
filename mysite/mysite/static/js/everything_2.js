var sample_data = ''

$.get("/api/get_me_the_torrents/", function(data) {
    sample_data = data
    // console.log(sample_data)
}).done(function() {
    displayTorrents(sample_data);
});

function displayTorrents(sample_data) {
    $(".resulting").html("");
    for (num in sample_data) {
        if (num < 10) {
            // tor_div = "<div class='torrent_info'><span class='tor_title'>"+sample_data[num].t_title+"</span><span class='number'>"+sample_data[num].t_seeders+"</span>"
            // $(".results").append(tor_div)
            tor_div = "<div class='torrent_info'><span class='tor_title'>"+sample_data[num].t_title+"</span><span class='number'></span>"
            tor_info_div = "<div class='result_info'>"+
              "<div class='tor_info' id='tor_category'>Category: "+sample_data[num].t_category+"</div>"+
              "<div class='tor_info' id='tor_website'>Website: "+sample_data[num].t_website+"</div>"+
              "<div class='tor_info' id='tor_url'>URL: "+sample_data[num].t_url+"</div>"+
              // "<div class='tor_info' id='tor_age'>Age: "+sample_data[num].t_age+"</div>"+
              "<div class='tor_info' id='tor_size'>Size: "+sample_data[num].t_size+" "+sample_data[num].t_sizeType+"</div>"+
              // "<div class='tor_info' id='tor_seeders'>Seeders: "+sample_data[num].t_seeders+"</div>"+
              // "<div class='tor_info' id='tor_leechers'>Leechers: "+sample_data[num].t_leechers+"</div>"+
              "</div></div>";
            $(".resulting").append(tor_div+tor_info_div)
        }
    }
}

//Cuts off part of the title

  // $(".tor_title").each(function(i){
  //   len=$(this).text().length;
  //   if(len>40)
  //   {
  //     $(this).text($(this).text().substr(0,40)+'...');
  //   }
  // });

$(function() {

    $("body").on("click", ".tor_title", function(e) {
        // console.log($(this).siblings()[1])
        $($(this).siblings()[1]).toggle();
    });

    $("body").on("click", "#resultstab", function(e) {
        // $("#filtertab").css('background-color', '#343A3D');
        // $("#resultstab").css('background-color', '#777');

        $("#filtertab").css('border', 'none');
        $("#filtertab").css('color', '#777');
        $("#resultstab").css('border-color', '#777');
        $("#resultstab").css('border-style', 'dashed');
        $("#resultstab").css('border-width', '1px');
        $("#resultstab").css('border-bottom', 'none');
        $("#resultstab").css('color', 'white');

        $(".results").toggle();
        $(".filter_options").toggle();
        $(".paging_thing").toggle();
    });

    $("body").on("click", "#filtertab", function(e) {
        // $("#resultstab").css('background-color', '#343A3D');
        // $("#filtertab").css('background-color', '#777');

        $("#resultstab").css('border', 'none');
        $("#resultstab").css('color', '#777');
        $("#filtertab").css('border-color', '#777');
        $("#filtertab").css('border-style', 'dashed');
        $("#filtertab").css('border-width', '1px');
        $("#filtertab").css('border-bottom', 'none');
        $("#filtertab").css('color', 'white');

        $(".filter_options").toggle();
        $(".results").toggle();
        $(".paging_thing").toggle();
    });

    $('.pagination').jqPagination({
        max_page: 20,
        paged: function(page) {
            lower_bound = (page-1)*10
            upper_bound = page*10

            temp_url = '/api/filter_by_checkboxes/'+lower_bound+'/'
            for (c in checkboxes) {
                val = checkboxes[c]
                // console.log($('.'+val).prop('checked'))
                temp_str = $('.'+val).prop('checked')
                if (temp_str==true) {
                    temp_url += 't/'
                } else {
                    temp_url += 'f/'
                }
            }

            input_val = $('.title_filter').val()
            temp_url += input_val

            console.log(temp_url)

            $.ajax({
                type: 'get',
                url: temp_url,
                success: function(data) {
                    displayTorrents(data['torrents'])
                    console.log(data)
                }
            });

            // $.ajax({
            //     type: 'get',
            //     url: '/api/get_paged_torrents/'+lower_bound,
            //     // data: lower_bound+'/'+upper_bound,
            //     // data: 'lb='+lower_bound,
            //     success: function(data) {
            //         displayTorrents(data)
            //     }
            // });
        }
    });

    $('.btn-group').button()

    var checkboxes=['books', 'music', 'movies', 'tv', 'pirate', 'kat', 'seedpeer'];

    $('body').on("click", '.filterbutton', function(e) {

        temp_url = '/api/filter_by_checkboxes/0/'
        for (c in checkboxes) {
            val = checkboxes[c]
            // console.log($('.'+val).prop('checked'))
            temp_str = $('.'+val).prop('checked')
            if (temp_str==true) {
                temp_url += 't/'
            } else {
                temp_url += 'f/'
            }
        }
        input_val = $('.title_filter').val()
        temp_url += input_val

        console.log(temp_url)

        $.ajax({
            type: 'get',
            url: temp_url,
            success: function(data) {
                console.log("success!")
                displayTorrents(data['torrents'])
                $(".first").click();
                console.log(data)
                update_heatmap(data['locations'])
            }
        });

    })


});
