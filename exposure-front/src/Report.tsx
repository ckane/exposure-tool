import { useParams } from 'react-router-dom'
import { Button } from '@mui/material'
import { Link } from 'react-router-dom'
import ReportContent from './ReportContent'

function Report() {
  const params = useParams();
  //console.log(params);
  return (
    <div>
      <h1>Report</h1>
      <ReportContent id={params.rpt} />
      <p>
       <Link to="/">
        <Button variant="contained" color="primary">Return to Listing</Button>
       </Link>
      </p>
    </div>
  )
}

export default Report;
