$(document).ready(function() {
    Highcharts.setOptions({
        colors: [ '#212529', '#343a40', '#495057', '#6c757d', '#adb5bd', '#ced4da', '#dee2e6', '#e9ecef', '#f8f9fa', '#A9927D'],        
    });
    Highcharts.chart("piechart", {
        chart: {
            backgroundColor: 'rgba(0,0,0,0)',
            plotBackgroundColor: 'rgba(0,0,0,0)',
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                enabled: false,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                },
                showInLegend: true
            }
        },
        legend: {
			enabled: true,
            itemStyle: {
                color: 'black'
             },
		},
        
        series: [{
            name: 'Allocation',
            colorByPoint: true,
            data : pie_data
            // data: [{
            //     name: 'BTC',
            //     y: 61.41,
            //     sliced: true,
            //     // selected: true
            // }, {
            //     name: 'ETH',
            //     // sliced: true,
            //     y: 11.84
            // }, {
            //     name: 'SOL',
            //     y: 10.85
            // }, {
            //     name: 'BNB',
            //     y: 4.67
            // }, {
            //     name: 'USDC',
            //     y: 4.18
            // }, {
            //     name: 'MATIC',
            //     y: 1.64
            // }, {
            //     name: 'LINK',
            //     y: 1.6
            // }, {
            //     name: 'XLM',
            //     y: 1.2
            // }, {
            //     name: 'USD',
            //     y: 2.61
            // }]
        }]
    });
});	