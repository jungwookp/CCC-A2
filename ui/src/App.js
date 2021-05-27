import React from 'react';

import AppBar  from './Appbar';
import InputModal from './ParameterModel';
import Content from './Content';

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

function App() {

  const [ title, setTitle ] = React.useState("CCC-Demo");
  const [ modalOpen, setModalOpen ] = React.useState(false);
  const [ baselineText, setBaselineText ] = React.useState();
  const [ plotType, setPlotType ] = React.useState();

  return (
    <React.Fragment>
      <React.Fragment>
        <AppBar position="fixed" title={title} openModel={()=>{ setModalOpen(true) }}/>
        <InputModal open={modalOpen} handleClose={()=>{setModalOpen(false)}} 
                    onConfirm={(title)=>{ setTitle(title) }} 
                    onSetBaseline={(bs)=>{ setBaselineText(bs) }}
                    onSetPlotType={setPlotType}
                    />
      </React.Fragment>
      <Content title={title} baseline={baselineText} plotType={plotType} />
    </React.Fragment>
  )
}
export default App;
