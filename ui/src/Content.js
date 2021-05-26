import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

import {word2vec, getAnalysisResult} from './conn';

import Plot from "./Plot";

const useStyles = makeStyles((theme) => ({
    content: {
        padding: theme.spacing(2),
        textAlign: 'center',
    },
    input: {
        width: 300
    }
}));


export default function Content(props) {
    const classes = useStyles();
    const {baseline, title} = props;

    // useEffect(() => {
    //     word2vec(baseline).then((vec) => {
    //         console.log(vec);
    //     })
    //     getAnalysisResult(baseline).then(rst=>console.log(rst));
    // }, [baseline]);

    return (
        <React.Fragment>
            <Grid container spacing={2} className={classes.content}>
                <Grid item xs={12}> <Typography variant="h4"> {title}  </Typography>  </Grid>
                <Grid item xs={12}> <Plot baseline={baseline} />  </Grid>
                <Grid item xs={12}> <Typography variant="h4"> {baseline}  </Typography>  </Grid>
            </Grid>
        </React.Fragment>
    )
}