import React from 'react';

import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

import AppBar  from './Appbar';
import InputModal from "./ParameterModel";
import Plot from "./Plot";

import './App.css';

/*
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
*/

const useStyles = makeStyles((theme) => ({
  content: {
      padding: theme.spacing(2),
      textAlign: 'center',
  },
  input: {
      width: 300
  }
}));

function App() {
  const classes = useStyles();

  const [title, setTitle] = React.useState("CCC-Demo");
  const [modalOpen, setModalOpen] = React.useState(false);
  const [ baselineText, setBaselineText ] = React.useState()

  

  return (
    <React.Fragment>
      <React.Fragment>
        <AppBar position="fixed" title={title} openModel={()=>{ setModalOpen(true) }}/>
        <InputModal open={modalOpen} handleClose={()=>{setModalOpen(false)}} 
                    onConfirm={(title)=>{ setTitle(title) }} 
                    onSetBaseline={(bs)=>{ setBaselineText(bs) }}
                    />
      </React.Fragment>
      <React.Fragment>
        <Grid container spacing={2} className={classes.content}>
          <Grid item xs={12}> <Typography variant="h4"> {title}  </Typography>  </Grid>
          <Grid item xs={12}> <Plot baseline={baselineText} />  </Grid>
          <Grid item xs={12}> <Typography variant="h4"> {baselineText}  </Typography>  </Grid>
        </Grid>
      </React.Fragment>
    </React.Fragment>
  )
}
export default App;
