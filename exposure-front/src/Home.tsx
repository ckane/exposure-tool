import { Link } from 'react-router-dom'
import Button from '@mui/material/Button'
import AssessmentsList from './AssessmentsList.tsx'

function Home() {
    return (
        <div>
            <h1>Assessments</h1>
            <Link to="/upload">
                <Button variant="contained" color="primary">Upload New Assessment File</Button>
            </Link>
            <p>Below is a list of (max 10) most recent assessments that have been uploaded</p>
            <AssessmentsList />
        </div>
    );
}

export default Home;
