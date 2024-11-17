import useSWR from 'swr';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

const fetcher = (url: string) => fetch(url).then(res => res.json());

type NodeData = {
    id: number;
    name: string;
    latency: number;
}

const LatencyTable = ({ selectedIDs }: { selectedIDs: String[] }) => {
    const { data, error, isLoading } = useSWR<NodeData[]>('http://localhost:8000/nodes', fetcher);
    if (isLoading) return <div>Loading...</div>
    if (error) return <div>Error loading data: {JSON.stringify(error)}</div>

    console.log("Got nodes: ", data);
    
    return <Table className="h-full  ">
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[160px]">Producer</TableHead>
                  <TableHead className="w-[160px]">Consumer</TableHead>
                  <TableHead className="text-right">Average Latency (ms)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {
                selectedIDs.filter((id) => id.includes("-")).map((id: String) => {
                    const [a, b] = id.split("-");
                    
                    const n1 = data?.find((node) => node.id === parseInt(a));
                    const n2 = data?.find((node) => node.id === parseInt(b));
                    if (!n1 || !n2) {
                        console.log("Node not found: ", id, n1, n2);
                        return null;
                    } else {
                        console.log("Node found: ", id, n1, n2);
                    }

                    return (
                      <TableRow key={n1.id}>
                        <TableCell>{n1.name}</TableCell>
                        <TableCell>{n2.name}</TableCell>
                        <TableCell className="text-right">{n1.latency}</TableCell>
                      </TableRow>
                    )
                  })
                }  
              </TableBody>
            </Table>
}

export {LatencyTable};