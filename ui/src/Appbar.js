import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: 'auto',
    marginLeft: 'auto',
  },
  title: {
    flexGrow: 1,
  },
  modalButton: {
  },
}));

export default function ButtonAppBar(props) {
  const classes = useStyles();
  const { title, openModel} = props;

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            CCC-DEMO
          </Typography>
          <Typography variant="h6" className={classes.title}>
            {title}
          </Typography>
          <Button color="inherit" className={classes.modalButton} onClick={openModel}>New Analysis</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}