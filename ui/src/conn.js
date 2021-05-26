

export const UI_BACKENT = "http://localhost:8944";
export const ENDPOINT_ANALYSIS = `${UI_BACKENT}/analysis`; 
export const ENDPOINT_WORD2VEC = `${UI_BACKENT}/word2vec`;


export async function getAnalysisResult( baseline ) {
    let response = await fetch(ENDPOINT_ANALYSIS, {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({
            baseline: baseline,
        }),
    });
    let rst = await response.json()
    return rst;
}

export async function word2vec( text ) {
    let response = await fetch(ENDPOINT_WORD2VEC, {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({
            data: text,
        }),
    });
    let rst = await response.json()
    return rst["data"];
}