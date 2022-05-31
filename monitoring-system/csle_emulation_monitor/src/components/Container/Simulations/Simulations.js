import React, {useState, useEffect, useCallback, createRef} from 'react';
import './Simulations.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Accordion from 'react-bootstrap/Accordion';
import Spinner from 'react-bootstrap/Spinner'
import MarkovChain from './Markov.png'
import Simulation from "./Simulation/Simulation";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import { useDebouncedCallback } from 'use-debounce';

const Simulations = () => {
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [simulations, setSimulations] = useState([]);
    const [filteredSimulations, setFilteredSimulations] = useState([]);
    const [searchString, setSearchString] = useState("");
    const [loading, setLoading] = useState(true);
    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchSimulations = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSimulations(response);
                setFilteredSimulations(response);
                setLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSimulationsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/simulationsdata/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSimulations()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchSimulations();
    }, [fetchSimulations]);


    const removeSimulationRequest = useCallback((simulation_name) => {
        fetch(
            `http://` + ip + ':7777/simulationsdata/remove/' + simulation_name,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchSimulations()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeSimulation = (simulation) => {
        setLoading(true)
        removeSimulationRequest(simulation.name)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload simulations from the backend
        </Tooltip>
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the simulation environments
        </Tooltip>
    );

    const renderRemoveAllSimulationsTooltop = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all simulations.
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        fetchSimulations()
    }

    const removeAllSimulations = () => {
        setLoading(true)
        removeAllSimulationsRequest()
    }

    const searchFilter = (simulation, searchVal) => {
        return (searchVal === "" ||
            simulation.id.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            simulation.name.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1 ||
            simulation.descr.toLowerCase().indexOf(searchVal.toString()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredSims = simulations.filter(simulation => {
            return searchFilter(simulation, searchVal)
        });
        setFilteredSimulations(filteredSims)
        setSearchString(searchVal)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Simulations
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Simulation of emulated infrastructures</h4>
                    <p className="modalText">
                        A simulation is defined as a Markov decision process or stochastic game, which models
                        how a discrete-time dynamical system is evolved and can be controlled.
                    </p>
                    <div className="text-center">
                        <img src={MarkovChain} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SimulationAccordions = (props) => {
        if (props.loading) {
            return (
                <Spinner animation="border" role="status">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    {props.simulations.map((simulation, index) =>
                        <Simulation simulation={simulation} wrapper={wrapper} key={simulation.name + "-" + index}
                                    removeSimulation={removeSimulation}
                        />
                    )}
                </Accordion>
            )
        }
    }

    const wrapper = createRef();

    return (
        <div className="Simulations">
            <div className="row">
                <div className="col-sm-3"></div>
                <div className="col-sm-3">
                    <h3> Simulations

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRefreshTooltip}
                        >
                            <Button variant="button" onClick={refresh}>
                                <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderInfoTooltip}
                        >
                            <Button variant="button" onClick={() => setShowInfoModal(true)}>
                                <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                        <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                        <OverlayTrigger
                            placement="top"
                            delay={{show: 0, hide: 0}}
                            overlay={renderRemoveAllSimulationsTooltop}
                        >
                            <Button variant="danger" onClick={removeAllSimulations}>
                                <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                            </Button>
                        </OverlayTrigger>
                    </h3>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <SimulationAccordions loading={loading} simulations={filteredSimulations}/>
        </div>
    );
}

Simulations.propTypes = {};
Simulations.defaultProps = {};
export default Simulations;