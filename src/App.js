import logo from './logo.svg';
//import './App.css';
import FileUpload from './handlers/file_upload'
import FileList from './handlers/FileList';
import MyComponent from './handlers/FileFetcher';
import FetchFileNames from './handlers/FetchFileNames';

function App() {
  return (
    <div className="App">
      <header className="App-header"> </header>

      <body>
        <FileUpload/>  
        <FileList/> 
{/*        <MyComponent/>
*/}      </body>
    </div>
  );
}

export default App;
