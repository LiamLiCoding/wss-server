let labelPercentFormatter = function(value) {
    return value + "%";
};
let labelUnitFormatter = function(value) {
    if (value >= 1048576) {
        value = Math.ceil(value / 1048576) + " MB";
    }
    else if(value >= 1024){
        value = Math.ceil(value / 1024) + " KB";
    }
  return value;
};

let optionsCPUUsedArea = {
    series: [],
    chart: {
        id: 'cpu',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'CPU Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    colors: ['#4B38AA'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        min:0,
        max:100,
        tickAmount: 2,
        title: {text:"Utilization Rate(%)"},
         labels: {
            formatter: labelPercentFormatter
         }
    },
    xaxis: {
        type: 'datetime',
        labels: {
            formatter: function(value, timestamp, opts) {
              return opts.dateFormatter(new Date(timestamp), 'HH:mm:ss')
            }
        },
    }
};
let CPUUsedArea = new ApexCharts(document.querySelector("#cpu-used-area"), optionsCPUUsedArea);

let optionsMemUsedArea = {
    series: [],
    chart: {
        id: 'memory',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'Memory Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    colors: ['#FFBE0B'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        min:0,
        max:100,
        tickAmount: 2,
        title: {text:"Utilization Rate(%)"},
        labels: {
            formatter: labelPercentFormatter
        }
    },
    xaxis: {
        type: 'datetime',
        labels: {
            formatter: function(value, timestamp, opts) {
              return opts.dateFormatter(new Date(timestamp), 'HH:mm:ss')
            }
        },
    }
};
let MemUsedArea = new ApexCharts(document.querySelector("#memory-used-area"), optionsMemUsedArea);

let optionsDiskIOArea = {
    series: [],
    chart: {
        id: 'disk',
        group: 'op_status',
        type: 'area',
        height: 200,
        zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    title: {
        text: 'Disk Used',
        align: 'center',
        style: {
            fontWeight: 500,
        },
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
        },
    },
    colors: ['#45CB85', '#F06548'],
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    toolbar: {
        tools: {
            selection: false
        }
    },
    markers: {
        size: 0
    },
    tooltip: {
        followCursor: false,
        x: {
            show: false
        },
        marker: {
            show: false
        },
        y: {
            title: {
                formatter: function () {
                    return ''
                }
            }
        }
    },
    grid: {
        clipMarkers: false
    },
    yaxis: {
        tickAmount: 2,
        title: {text:"Disk IO(K)"},
         labels: {
            formatter: labelUnitFormatter
          }
    },
    xaxis: {
        type: 'datetime'
    }
};
let diskIOArea = new ApexCharts(document.querySelector("#disk-used-area"), optionsDiskIOArea);

let performance_url = $("#performance-chart").data("urls");

let updateChartData = function () {
    $.getJSON(performance_url, function(response) {
        let cpu_data = [];
        let mem_data = [];
        let disk_write_io_data = [];
        let disk_read_io_data = [];
        for(let each_data of response){
            cpu_data.push({x:each_data['created_time'], y:each_data['cpu_rate']});
            mem_data.push({x:each_data['created_time'], y:each_data['mem_rate']});
            disk_write_io_data.push({x:each_data['created_time'], y:each_data['disk_write_io']});
            disk_read_io_data.push({x:each_data['created_time'], y:each_data['disk_read_io']});
        }
        CPUUsedArea.updateSeries([{data: cpu_data}]);
        MemUsedArea.updateSeries([{data: mem_data}]);
        diskIOArea.updateSeries([
            {
                name: 'Write IO',
                data: disk_write_io_data,
            },
            {
                name: 'Read IO',
                data: disk_read_io_data,
            },
        ]);
    });
};

// Performance charts
if ($('#performance-no-result').length === 0) {
    CPUUsedArea.render();
    MemUsedArea.render();
    diskIOArea.render();
    updateChartData()
    window.setInterval("updateChartData()", 5000);
}

// Event log and Operation log table
let event_log_url= $("#event-log").data("urls");
let operation_log_url= $("#operation-log").data("urls");

let updateEventLog = function () {
    $.ajax({
        type: 'get',
        url: event_log_url,
        data: {page: even_log_page.current},
        success: function (data) {
            if(data.next){
                even_log_page.next=true;
                $('#event-log-next').removeClass("disabled");
            }
            else{
                even_log_page.next=false;
                $('#event-log-next').addClass("disabled");
            }
            if(data.previous){
                even_log_page.previous=true;
                $('#event-log-previous').removeClass("disabled");
            }
            else{
                even_log_page.previous=false;
                $('#event-log-previous').addClass("disabled");
            }
            if(data.count === 0){
                $('#event-log-noresult').css("display", "inline");
                $('#event-log-table').css("display", "none");
                $('#event-image-noresult').css("display", "inline");
                $('#event-image').css("display", "none");
            }
            else{
                $('#event-log-noresult').css("display", "none");
                $('#event-log-table').css("display", "inline");
                $('#event-image-noresult').css("display", "none");
                $('#event-image').css("display", "inline");

                let event_table_html = ''
                let event_image_html = '';
                let event_type_color = {2: 'text-bg-info', 3: 'text-bg-primary', 4: 'text-bg-danger'};
                for(let each_log of data.results){
                    event_table_html += `<tr>
                        <th scope="row"><span class="badge ${event_type_color[each_log.event]}">Event${each_log.event}</span></th>
                        <td>${each_log.message}</td>
                        <td>${each_log.action}</td>
                        <td><a target="_blank" href="${each_log.image_url}"><u>Preview</u></a></td>
                        <td>${each_log.created_time}</td>
                    </tr>`

                    event_image_html += `
                        <div class="col-xl-4 col-sm-6">
                            <div class="gallery-box card">
                                <div class="gallery-container">
                                    <a class="event-image-gallery" href="${each_log.image_url}">
                                        <img class="gallery-img img-fluid mx-auto" src="${each_log.image_url}" alt="" />
                                        <div class="gallery-overlay">
                                            <h5 class="overlay-caption">Event${each_log.event}</h5>
                                        </div>
                                    </a>
                                </div>

                                <div class="box-content">
                                    <div class="d-flex align-items-center mt-1">
                                        <div class="flex-grow-1 text-body text-truncate">${each_log.message}</div>
                                        <div class="flex-shrink-0 text-body text-truncate">${each_log.created_time}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- end col -->
                    `
                }
                $('#event-log-tbody').html(event_table_html);
                $('#event-image-container').html(event_image_html);
                // Image pop up initial
                const  event_image_gallery = GLightbox({
                    selector: '.event-image-gallery',
                    title: false,
                });
            }
        }
    });
}

let updateOperationLog = function () {
    $.ajax({
        type: 'get',
        url: operation_log_url,
        data: {page: operation_log_page.current},
        success: function (data) {
            if(data.next){
                operation_log_page.next=true;
                $('#operation-log-next').removeClass("disabled");
            }
            else{
                operation_log_page.next=false;
                $('#operation-log-next').addClass("disabled");
            }
            if(data.previous){
                operation_log_page.previous=true;
                $('#operation-log-previous').removeClass("disabled");
            }
            else{
                operation_log_page.previous=false;
                $('#operation-log-previous').addClass("disabled");
            }
            if(data.count === 0){
                $('#operation-log-noresult').css("display", "inline");
                $('#operation-log-table').css("display", "none");
            }
            else{
                $('#operation-log-noresult').css("display", "none");
                $('#operation-log-table').css("display", "inline");
                let operation_table_html = '';
                for(let each_log of data.results){
                    operation_table_html += `<tr>
                        <th scope="row"><span class="badge text-bg-danger fs-15">${each_log.operation}</span></th>
                        <td>${each_log.message}</td>
                        <td>${each_log.created_time}</td>
                    </tr>`
                }
                $('#operation-log-tbody').html(operation_table_html);
            }
        }
    });
}

let even_log_page = {current:1, next:false, previous:false, func:updateEventLog};
let operation_log_page = {current:1, next:false, previous:false, func:updateOperationLog};

function page_change(type, is_add) {
    let page = type === 'event' ? even_log_page : operation_log_page;
    if(is_add && page.next){
        page.current += 1;
        page.func();
    }
    else if(!is_add && page.previous){
        page.current -= 1;
        page.func();
    }
    return true
}

updateEventLog();
updateOperationLog();

// Operation Modals
let url = '';
let operation = '';
let operation_type = '';

$('#operation_modal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    operation_type = button.data('operation_type');
    operation = button.data('operation');
    url = $(this).data('urls');
    if (operation_type === 'restart'){
        $('#operation-modal-title').text(`You are about to restart the device`);
        $('#operation-modal-icon').attr("src", "https://cdn.lordicon.com/wrprwmwt.json");
    }
    else if(operation_type === 'profiler'){
        $('#operation-modal-title').text(`You are about to ${operation} Profiler`);
        $('#operation-modal-icon').attr("src", "https://cdn.lordicon.com/rivoakkk.json");
    }
    else if(operation_type === 'intruder_detect'){
        $('#operation-modal-title').text(`You are about to ${operation} Intruder detection`);
        $('#operation-modal-icon').attr("src", "https://cdn.lordicon.com/rivoakkk.json");
    }
})
$('#operation_confirm').click(function (){
    $.ajax({
        type: 'post',
        url: url,
        data: {
            'operation': operation,
            'operation_type': operation_type,
            'message':$('#operation_message').val()},
    })
})

// Device Online time
let onlineTimeNode = $('#device_online_time');
if (onlineTimeNode.length !== 0){
    let timeString = onlineTimeNode.data('online-time');
    let timeLogin = new Date(timeString).getTime();
    let resultString = '';
    let updateOnlineTime = setInterval(function () {

        let currentTime = new Date().getTime();
        let distance = currentTime - timeLogin;

        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);
        if (days >= 1){
            resultString = days + ' Day ' + hours + ' Hour ' + minutes + ' Min ';
        }
        if(hours >= 1){
            resultString = hours + ' Hour ' + minutes + ' Min ' + seconds +' sec ';
        }
        else{
            resultString =  minutes + ' min ' + seconds +' sec ';
        }

        onlineTimeNode.html(resultString);
    }, 1000)
}

