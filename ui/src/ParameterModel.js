import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles((theme) => ({
    paper: {
        marginLeft: "auto",
        marginRight: "auto",
        marginTop: "auto",
        marginBottom: "auto",

        width: 400,
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),

        textAlign: 'center',
    },
    input: {
        width: 300
    }
  }));


export default function ParameterModal(props) {
    const classes = useStyles();
    const { open, handleClose, onConfirm, onSetBaseline, onSetPlotType } = props;

    const [title, setTitle] = React.useState("Untitled")
    const analysisTypeOptions = [
        { "value": "heat-map",
           "label": "Heat Map" },
        { "value": "regression",
        "label": "Regression" }
    ];
    const [analysisType, setAnalysisType] = React.useState(analysisTypeOptions[0].value)
    const [baseline, setBaseline] = React.useState()

    const titleInput = (
        <TextField
          id="analysis-title"
          label="Analysis Title"
          value={title}
          className={classes.input}
          onChange={(event)=>{ setTitle(event.target.value) }}
        />
    );

    const analysisTypeSelect = (
        <TextField
          id="analysis-type"
          className={classes.input}
          select
          label="Analysis Type"
          value={ analysisType }
          onChange={(event)=>{ setAnalysisType(event.target.value) }}
        >
          { 
            analysisTypeOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                {option.label}
                </MenuItem>
            ))
           }
        </TextField>)

    const baselineInput = (
        <TextField
        id="baseline"
        label="Baseline"
        value={baseline}
        className={classes.input}
        onChange={(event)=>{ setBaseline(event.target.value) }}
        multiline
        />
    );

    const body = (
        <Paper className={classes.paper}>
          <Grid container spacing={5}>
            <Grid item xs={12}> <Typography variant="h4"> Analysis Parameters </Typography>  </Grid>
            <Grid item xs={12}> {titleInput} </Grid>
            <Grid item xs={12}> {baselineInput} </Grid>
            <Grid item xs={12}> <Typography> {analysisTypeSelect} </Typography>  </Grid>
            <Grid item xs={5}>  <Button variant="contained" color="primary"
                                        onClick={()=>{
                                          onConfirm(title);
                                          onSetBaseline(baseline);
                                          onSetPlotType(analysisType)
                                          handleClose(); }}> 
                                        Confirm
                                </Button> </Grid>
            <Grid item xs={2}>  </Grid>
            <Grid item xs={5}> 
              <Button variant="contained" onClick={ ()=>{ handleClose();  } }> Cancel </Button> 
            </Grid>
          </Grid>
        </Paper>
      );

    return (
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="simple-modal-title"
            aria-describedby="simple-modal-description">
            {body}
        </Modal>
    );
}