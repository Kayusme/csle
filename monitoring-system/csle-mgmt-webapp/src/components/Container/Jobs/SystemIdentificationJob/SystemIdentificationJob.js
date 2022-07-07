import React, {useState, useCallback} from 'react';
import './SystemIdentificationJob.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'
import Spinner from 'react-bootstrap/Spinner'

const SystemIdentificationJob = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [logsOpen, setLogsOpen] = useState(false);
    const [loadingLogs, setLoadingLogs] = useState(false);
    const [hyperparametersOpen, setHyperparametersOpen] = useState(false);
    const [logs, setLogs] = useState(null);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const renderRemoveSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove system identification job
        </Tooltip>);

    const renderStopSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop system identification job
        </Tooltip>);

    const renderStartSystemIdentificationJobTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start system identification job
        </Tooltip>);

    const getStatusText = () => {
        if (props.job.running) {
            return ("Running")
        } else {
            return ("Stopped")
        }
    }

    const getModelType = (model_type) => {
        if (model_type === 0) {
            return ("Gaussian mixture")
        } else {
            return ("Unknown")
        }
    }

    const getGreenOrRedCircle = () => {
        if (props.job.running) {
            return (<circle r="15" cx="15" cy="15" fill="green"></circle>)
        } else {
            return (<circle r="15" cx="15" cy="15" fill="red"></circle>)
        }
    }

    const fetchLogs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/file',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({path: props.job.log_file_path})
            }
        )
            .then(res => res.json())
            .then(response => {
                setLoadingLogs(false)
                setLogs(parseLogs(response))
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopButton = () => {
        if (props.job.running) {
            return (<OverlayTrigger
                placement="top"
                delay={{show: 0, hide: 0}}
                overlay={renderStopSystemIdentificationJobTooltip}
            >
                <Button variant="warning" className="startButton"
                        onClick={() => props.stopSystemIdentificationJob(props.job)}>
                    <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>)
        } else {
            return (<OverlayTrigger
                placement="top"
                delay={{show: 0, hide: 0}}
                overlay={renderStartSystemIdentificationJobTooltip}
            >
                <Button variant="success" className="startButton"
                        onClick={() => props.startSystemIdentificationJob(props.job)}>
                    <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                </Button>
            </OverlayTrigger>)
        }
    }

    const parseLogs = (logs) => {
        var lines = logs.logs.split("\n")
        var data = lines.map((line, index) => {
            var parts = line.split(/,(.*)/)
            var date = parts[0]
            var content = parts[1]
            return {
                date: date,
                content: content
            }
        })
        return data
    }

    const getLogs = () => {
        if (logsOpen) {
            setLogsOpen(false)
        } else {
            setLogsOpen(true)
            setLoadingLogs(true)
            fetchLogs()
        }
    }

    const SpinnerOrLogs = (props) => {
        if (props.loadingLogs || props.logs === null || props.logs === undefined) {
            return (<Spinner
                as="span"
                animation="grow"
                size="sm"
                role="status"
                aria-hidden="true"
            />)
        } else {
            return (
                <div className="table-responsive">
                    <Table striped bordered hover>
                        <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Log line</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.logs.map((logLine, index) => {
                            return <tr key={logLine.date + "-" + index}>
                                <td>{logLine.date}</td>
                                <td>{logLine.content}</td>
                            </tr>
                        })}
                        </tbody>
                    </Table>
                </div>
            )
        }

    }

    return (<Card key={props.job.id} ref={props.wrapper}>
            <Card.Header>
                <Accordion.Toggle as={Button} variant="link" eventKey={props.job.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.job.id}, Emulation: {props.job.emulation_env_name}</span>
                    Progress: {Math.round(100 * props.job.progress_percentage * 100) / 100}%
                    Status: {getStatusText()}
                    <span className="greenCircle">

                    <svg id="svg-1" height="15px" width="15px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"
                         version="1.1">
                    {getGreenOrRedCircle()}
                </svg></span>
                </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={props.job.id}>
                <Card.Body>
                    <h5 className="semiTitle">
                        Actions:
                        {startOrStopButton()}
                        <OverlayTrigger
                            className="removeButton"
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveSystemIdentificationJobTooltip}
                        >
                            <Button variant="danger" className="removeButton"
                                    onClick={() => props.removeSystemIdentificationJob(props.job)}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h5>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                                aria-controls="generalInfoBody"
                                aria-expanded={generalInfoOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle"> General Information about the system identification job</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={generalInfoOpen}>
                            <div id="generalInfoBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Attribute</th>
                                            <th> Value</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td>ID</td>
                                            <td>{props.job.id}</td>
                                        </tr>
                                        <tr>
                                            <td>PID</td>
                                            <td>{props.job.pid}</td>
                                        </tr>
                                        <tr>
                                            <td>Emulation</td>
                                            <td>{props.job.emulation_env_name}</td>
                                        </tr>
                                        <tr>
                                            <td>Log file path</td>
                                            <td>{props.job.log_file_path}</td>
                                        </tr>
                                        <tr>
                                            <td>Description</td>
                                            <td>{props.job.descr}</td>
                                        </tr>
                                        <tr>
                                            <td>Emulation statistic ID</td>
                                            <td>{props.job.emulation_statistics_id}</td>
                                        </tr>
                                        <tr>
                                            <td>System model type</td>
                                            <td>{getModelType(props.job.system_identification_config.model_type)}</td>
                                        </tr>
                                        <tr>
                                            <td>Title</td>
                                            <td>{props.job.system_identification_config.title}</td>
                                        </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={() => setHyperparametersOpen(!hyperparametersOpen)}
                                aria-controls="hyperparametersBody"
                                aria-expanded={hyperparametersOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle"> Hyperparameters</h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={hyperparametersOpen}>
                            <div id="hyperparametersBody" className="cardBodyHidden">
                                <div className="table-responsive">
                                    <Table striped bordered hover>
                                        <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Description</th>
                                            <th>Value</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {Object.keys(props.job.system_identification_config.hparams).map((hparamName, index) => {
                                            return <tr key={hparamName + "-" + index}>
                                                <td>{hparamName}</td>
                                                <td>{props.job.system_identification_config.hparams[hparamName].descr}</td>
                                                <td>{props.job.system_identification_config.hparams[hparamName].value}</td>
                                            </tr>
                                        })}
                                        </tbody>
                                    </Table>
                                </div>
                            </div>
                        </Collapse>
                    </Card>

                    <Card>
                        <Card.Header>
                            <Button
                                onClick={getLogs}
                                aria-controls="logsOpenBody"
                                aria-expanded={logsOpen}
                                variant="link"
                            >
                                <h5 className="semiTitle"> Logs: {props.job.log_file_path} </h5>
                            </Button>
                        </Card.Header>
                        <Collapse in={logsOpen}>
                            <div id="logsOpenBody" className="cardBodyHidden">
                                <SpinnerOrLogs loadingLogs={loadingLogs} logs={logs}/>
                            </div>
                        </Collapse>
                    </Card>

                </Card.Body>
            </Accordion.Collapse>
        </Card>
    )
}

SystemIdentificationJob.propTypes = {};
SystemIdentificationJob.defaultProps = {};
export default SystemIdentificationJob;