import { Link } from 'react-router-dom'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import './Upload.css'

const uploadHandler = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent the browser from submitting the form
    const data = new FormData(event.currentTarget);
    const file = data.get("file_upload") as File | null;
    const title = data.get("title") as string | null;

    // Check if a file was selected and title was given and upload it via the API
    if (file && title) {
      const formData = new FormData();
      formData.append("file_upload", file);
      formData.append("title", title);
      fetch("/api/uploadfile", {
        method: "POST",
        body: formData,
      }).then((response) => response.json())
            .then((data) => {
                const errormsg = document.getElementById("errormsg");
                if (errormsg) {
                    if (data.error) {
                        errormsg.innerText = data.message;
                    } else {
                        errormsg.innerText = "File uploaded successfully";
                    }
                }
            })
        .catch((error) => console.error("Error:", error));
    }
}

function Upload() {
    return (
        <div>
            <h1>Upload a new assessment file</h1>
            { /* A SPAN for a message to be displayed on async upload success/failure */ }
            <p><span id="errormsg"></span></p>
            <form onSubmit={(event) => uploadHandler(event)} >
             <p>Name of report: <TextField id="title" name="title" color="primary" sx={{ input: { color: 'white' } }}required></TextField></p>
             <p><TextField type="file" id="file_upload" name="file_upload" color="primary" sx={{ input: { color: 'white' }}} required></TextField></p>
             <p><Button type="submit" variant="contained" color="primary">Upload New Assessment File</Button></p>
            </form>
        <p>
            <Link to="/">
             <Button variant="contained" color="primary">Return to Listing</Button>
            </Link>
        </p>
        </div>
    );
}

export default Upload;
