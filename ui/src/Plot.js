import React from 'react';
import Plotly from 'plotly.js-dist';
import get_poly_center from './poly_center';
import gen_test_data from './test';


const mapboxToken = "pk.eyJ1IjoieXVuc2h1aSIsImEiOiJja3A0M2Q0dzUxeGpjMzJxcWxxd2NocWVzIn0.19wTZgELWgq3L2Apv8jVeQ"


Plotly.setPlotConfig({
    mapboxAccessToken: mapboxToken
})

const poly_center = get_poly_center()
const test_data = gen_test_data()

function get_locations(sa_codes) {
    let rst = sa_codes.map((code) => poly_center[code]);
    return rst
}

function get_test_trace() {
    // count data
    const list_data = []
    for (const [k, v] of Object.entries(test_data)) {
        list_data.push([k, v]);
    }

    const sa_codes = list_data.map((ele) => ele[0])
    const locations = get_locations(sa_codes)
    console.log(locations)
    const lat = locations.map(ele=>ele[1])
    const lon = locations.map(ele=>ele[0])

    const value = list_data.map((ele) => ele[1].count)
    const maxValue = Math.max(...value)
    const sizeScale = 100.0 / maxValue
    const colorScale = 50.0 / maxValue
    const size = value.map(ele => ele  * sizeScale);
    const color = value.map(ele => 10);

    return {
        type: 'scattermapbox',
        lat: lat,
        lon: lon,
        mode: "markers",
        marker: {
            size: size,
            color: color,
            colorscale: 'Greens',
            cmin: 0,
            cmax: 50,
            test: value,
        }
    }
}


export default function Plot(props) {
    const {baseline} = props
    const backend = "http://localhost:"
    React.useEffect(() => {

    });

    return (
        <div id="canvas">
        </div>
    )
}


function scatterGeo() {

    let data = [{
        type: 'scattergeo',
        mode: 'markers',
        locations: ['FRA', 'DEU', 'RUS', 'ESP'],
        marker: {
            size: [20, 30, 15, 10],
            color: [10, 20, 40, 50],
            cmin: 0,
            cmax: 50,
            colorscale: 'Greens',
            colorbar: {
                title: 'Some rate',
                ticksuffix: '%',
                showticksuffix: 'last'
            },
            line: {
                color: 'black'
            }
        },
        name: 'Melbourne data'
    }];

    let layout = {
        geo: {
            scope: 'world',
            resolution: 50,
            center: {
                lat: -37.840935,
                lon: 144.946457
            },
            projection: {
                scale: 50,
            },
        }
    };

    Plotly.newPlot('canvas', data, layout);
}


function scatterMapbox() {
    let test_trace = get_test_trace()
    let data = [test_trace]

    let layout = {
        autosize: true,
        hovermode: 'closest',
        mapbox: {
            bearing: 0,
            center: {
                lat: -37.840935,
                lon: 144.946457
            },
            pitch: 0,
            zoom: 10
        },
    }

    Plotly.newPlot('canvas', data, layout)
}