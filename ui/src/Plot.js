import React from 'react';
import Plotly from 'plotly.js-dist';
import get_poly_center from './poly_center';
import gen_test_data from './test';

import {  getAnalysisResult } from './conn';

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
        list_data.push([k, parseFloat(v)]);
    }
    const sa_codes = list_data.map((ele) => ele[0])
    const locations = get_locations(sa_codes)
    // console.log(locations)
    const lat = locations.map(ele => ele[1])
    const lon = locations.map(ele => ele[0])

    const value = list_data.map((ele) => ele[1].count)

    console.log({
        list_data: list_data,
        value: value
    })
    const maxValue = Math.max(...value)
    const sizeScale = 100.0 / maxValue
    // const colorScale = 50.0 / maxValue
    const size = value.map(ele => ele * sizeScale);
    console.log(size)
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


function get_trace(zone_to_value_data) {
    // count data
    const list_data = []
    for (const [k, v] of Object.entries(zone_to_value_data)) {
        list_data.push([k, parseFloat(v)]);
    }
    const sa_codes = list_data.map((ele) => ele[0])
    const locations = get_locations(sa_codes)
    // console.log(locations)
    const lat = locations.map(ele => ele[1])
    const lon = locations.map(ele => ele[0])

    let value = list_data.map((ele) => ele[1])
    
    const value_average = value.reduce((a, b) => a+b) / value.length;
    
    value = value.map(e => e - value_average);
    
    console.log({
        list_data: list_data,
        value: value
    });
    const maxValue = Math.max(...value);
    const minValue = Math.min(...value);
    const sizeScale = 5.0 / (maxValue - minValue);
    // const colorScale = 50.0 / maxValue
    const size = value.map(ele => Math.pow(2.2, (ele - minValue) * sizeScale));
    console.log(size)
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
    const { baseline, plotType } = props
    React.useEffect(() => {
        switch (plotType) {
            case "heat-map":
                if (!baseline) {
                    scatterMapbox(get_test_trace())
                } else {
                    getAnalysisResult(baseline)
                        .then(data => {
                            scatterMapbox(get_trace(data))
                        })
                }
                break;
            case "regression":
                break;
            default:
                console.log(`Unsupported plot type ${plotType}`)
                break;
        }
    }, [baseline, plotType]);

    return (
        <div id="canvas">
        </div>
    )
}


function scatterMapbox(trace) {
    let data = [trace]
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

function regression() {

}
