var finishedAlpha = 1;
var inProgressAlpha = 0;
var borderalpha= 0.8;
var ctx = document.getElementById("myChart").getContext(`2d`);


var colors = [
    'rgba(255, 70, 80, 1)',
    'rgba(75, 192, 130, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(153, 102, 255,1)',
    'rgba(255, 159, 64, 1)'
]
// var gradients = [];
// colors.forEach(element => {


//     var gradient = ctx.createLinearGradient(0, 0, 0, 400);
//     gradient.addColorStop(1, `${element} ${finishedAlpha})`);
//     // gradient.addColorStop(0.2, `rgba(255, 99, 132, ${inProgressAlpha})`);
//     // gradient.addColorStop(0.7,rgba(75, 192, 192, 0));
//     // ctx.fillStyle = gradient;
//     console.log(gradient);
//     gradients.push(gradient);
// });
Chart.defaults.global.defaultFontColor = 'silver';
var myChart = new Chart(ctx, {
    type: `bar`,
    data: {
        labels: [
            "Red", "Green ", "Blue", "Yellow"
        ],
        datasets: [
            {
                label: `Finished`,
                data: [
                    0, 0, 0, 0
                ],

                backgroundColor: colors,
                // hoverBackgroundColor : gradients,1)
                borderColor: [
                    `rgba(255,80,100,${borderalpha})`, `rgba(75, 192, 130, ${borderalpha})`, `rgba(54, 162, 235, ${borderalpha})`, `rgba(255, 206, 86, ${borderalpha})`,
                ],
                borderWidth: 4
            }, {
                label: `In Production`,
                data: [
                    0, 0, 0, 0
                ],
                backgroundColor: [
                    `rgba(255, 99, 132, ${inProgressAlpha})`, `rgba(75, 192, 192, ${inProgressAlpha})`, `rgba(54, 162, 235, ${inProgressAlpha})`, `rgba(255, 206, 86, ${inProgressAlpha})`,
                ],
                borderColor: [
                    `rgba(255,80,100,${borderalpha})`, `rgba(75, 192, 130, ${borderalpha})`, `rgba(54, 162, 235, ${borderalpha})`, `rgba(255, 206, 86, ${borderalpha})`,
                ],
                borderWidth: 4
            }
        ]
    },
    options: {
        scales: {
            
            xAxes: [
                {
                    stacked: true,
                    gridLines: {
                        display: false
                    }
                }
            ],
            yAxes: [
                {
                    stacked: true,
                    gridLines: {
                        color: 'gray'
                    },
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 10
                    }
                }
            ]

        }
    }
});

const socket = io('https://api.derimiksa.hu');

socket.on('telemetry', function(msg){
    console.log(msg)
});

socket.on('prodStats', function(prodStats){

    myChart.data.datasets[0].data = prodStats.map(e => parseInt(e.finished));
    myChart.data.datasets[1].data = prodStats.map(e => parseInt(e.inProgress));
    
	myChart.update();   
});
