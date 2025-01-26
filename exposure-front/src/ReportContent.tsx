import { useState, useEffect  } from 'react';
import { List, ListItem, ListItemButton, ListItemText } from '@mui/material'

function ReportContent({id}: {id: string}) {
  const [report, setReport] = useState({'resources': [], 'title': ''});
  const [resources, setResources] = useState([]);

  useEffect(() => {
      try {
          fetch(`/api/report/${id}`)
              .then(response => response.json())
              .then((data) => {
                  setResources(data.report.resources);
                  setReport(data.report);
              });
      } catch (error) {
          console.error('Failed to fetch report:', error);
      }
  }, [id]);

  return (
      <div>
      <b>{report.title}</b>
      <List>
          {resources.filter((rsrc) => rsrc.defects && rsrc.defects.length > 0).map((rsrc, index) => (
              <ListItem key={index}>
               <ListItemButton><ListItemText>
                <b>{rsrc['name']}: Defect Count: {rsrc.defects.length}</b>
                <ul>
                 {rsrc.defects.map((defect, defectIndex) => (
                     <li key={defectIndex}>{defect['type']}: {defect['message']}</li>
                 ))}
                </ul>
               </ListItemText></ListItemButton>
              </ListItem>
          ))}
      </List>
      </div>
  );
}

export default ReportContent;
