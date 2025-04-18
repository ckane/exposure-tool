import { useState, useEffect  } from 'react';
import { Link } from 'react-router-dom'
import { List, ListItem, ListItemButton, ListItemText } from '@mui/material'

function ListContents() {
    /* fetch the list contents dynamically from the "reports" key of the API /api/list call */
    const [reports, setReports] = useState([]);

    useEffect(() => {
        fetch('/api/list')
            .then(response => response.json())
            .then(data => {
                if (data && data.reports) {
                    setReports(data.reports);
                }
            });
    }, []);

    /* Generate the list and its contents. */
    return (
        <List>
            {reports.map((report, index) => (
                <ListItem key={index}><Link to={`/report/${report['digest']}`}>
                  <ListItemButton><ListItemText>{report['date']}: {report['name']}</ListItemText></ListItemButton>
                </Link></ListItem>
            ))}
        </List>
    );
}

function AssessmentsList() {
    return (
        <div>
            <ListContents />
        </div>
    );
}

export default AssessmentsList;
