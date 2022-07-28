import React, {useState, useEffect, useCallback} from 'react';
import "rc-slider/assets/index.css";
import './Monitoring.css';
import Select from 'react-select'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Modal from 'react-bootstrap/Modal'
import ContainerMetrics from "./ContainerMetrics/ContainerMetrics";
import AggregateMetrics from "./AggregateMetrics/AggregateMetrics";
import OpenFlowSwitchesStats from "./OpenFlowSwitchesStats/OpenFlowSwitchesStats";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import DataCollection from './MonitoringSetup.png'
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {useDebouncedCallback} from 'use-debounce';
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";

const Monitoring = (props) => {
    const windowLengthOptions = [
        {
            value: 15,
            label: "15 min"
        },
        {
            value: 30,
            label: "30 min"
        },
        {
            value: 60,
            label: "1h"
        },
        {
            value: 120,
            label: "2h"
        },
        {
            value: 240,
            label: "4h"
        },
        {
            value: 480,
            label: "8h"
        },
        {
            value: 960,
            label: "16h"
        },
        {
            value: 1920,
            label: "32h"
        },
        {
            value: 3840,
            label: "64h"
        },
    ]
    const evolutionSpeedOptions = [
        {
            value: 0,
            label: "No animation"
        },
        {
            value: 1,
            label: "1%"
        },
        {
            value: 25,
            label: "25%"
        },
        {
            value: 50,
            label: "50%"
        },
        {
            value: 75,
            label: "75%"
        },
        {
            value: 100,
            label: "100%"
        }
    ]
    const [emulationExecutionIds, setEmulationExecutionIds] = useState([]);
    const [filteredEmulationExecutionIds, setFilteredEmulationExecutionIds] = useState([]);
    const [emulationExecutionContainerOptions, setEmulationExecutionContainerOptions] = useState([]);
    const [selectedEmulationExecutionId, setSelectedEmulationExecutionId] = useState(null);
    const [selectedEmulationExecution, setSelectedEmulationExecution] = useState(null);
    const [windowLength, setWindowLength] = useState(windowLengthOptions[0]);
    const [selectedContainer, setSelectedContainer] = useState(null);
    const [monitoringData, setMonitoringData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationExecution, setLoadingSelectedEmulationExecution] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(evolutionSpeedOptions[0]);
    const [animation, setAnimation] = useState(false);
    const animationDurationFactor = 50000
    const [grafanaStatus, setGrafanaStatus] = useState(null);
    const [cAdvisorStatus, setCAdvisorStatus] = useState(null);
    const [prometheusStatus, setPrometheusStatus] = useState(null);
    const [nodeExporterStatus, setNodeExporterStatus] = useState(null);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [searchString, setSearchString] = useState("");
    const [openFlowSwitchesOptions, setOpenFlowSwitchesOptions] = useState([]);
    const [selectedOpenFlowSwitch, setSelectedOpenFlowSwitch] = useState(null);
    const ip = "localhost"
    const alert = useAlert();
    const navigate = useNavigate();

    // const ip = "172.31.212.92"

    const animationDurationUpdate = (selectedObj) => {
        setAnimationDuration(selectedObj)
        if (selectedObj.value > 0) {
            setAnimation(true)
        } else {
            setAnimation(false)
        }
    };

    const getDockerMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.docker_host_stats[selectedContainer.label]
        } else {
            return null
        }
    }

    const getHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.host_metrics[selectedContainer.label]
        } else {
            return null
        }
    }

    const getPortStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch != null) {
            return monitoringData.openflow_port_avg_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getAggFlowStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch != null) {
            return monitoringData.agg_openflow_flow_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getFlowStats = () => {
        if (monitoringData !== null && selectedOpenFlowSwitch !== null) {
            return monitoringData.openflow_flow_avg_metrics_per_switch[selectedOpenFlowSwitch.label]
        } else {
            return null
        }
    }

    const getSnortIdsMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.snort_ids_metrics
        } else {
            return null
        }
    }

    const getOSSECHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.ossec_host_alert_counters[selectedContainer.label]
        } else {
            return null
        }
    }

    const getAggregatedOSSECHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_ossec_host_alert_counters
        } else {
            return null
        }
    }

    const getClientMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.client_metrics
        } else {
            return null
        }
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload emulations and monitoring data from the backend
        </Tooltip>
    );

    const getAggregatedDockerStats = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_docker_stats
        } else {
            return null
        }
    }

    const getAggregatedHostMetrics = () => {
        if (monitoringData !== null) {
            return monitoringData.aggregated_host_metrics
        } else {
            return null
        }
    }

    const onChangeWindowLength = (windowLenSelection) => {
        if (windowLenSelection.value !== windowLength) {
            setWindowLength(windowLenSelection)
            setLoadingSelectedEmulationExecution(true)
            fetchMonitoringData(windowLength.value, selectedEmulationExecution)
        }
    }

    const updateEmulationExecutionId = (emulationExecutionId) => {
        setSelectedEmulationExecutionId(emulationExecutionId)
        fetchSelectedExecution(emulationExecutionId)
        setLoadingSelectedEmulationExecution(true)
        setMonitoringData(null)
    }

    const updateHost = (container) => {
        setSelectedContainer(container)
    }

    const updateOpenFlowSwitch = (openFlowSwitch) => {
        setSelectedOpenFlowSwitch(openFlowSwitch)
    }

    const refresh = () => {
        setLoading(true)
        setLoadingSelectedEmulationExecution(true)
        setSelectedEmulationExecution(null)
        fetchGrafanaStatus()
        fetchPrometheusStatus()
        fetchCadvisorStatus()
        fetchNodeExporterStatus()
        fetchEmulationExecutionIds()
    }

    const searchFilter = (executionIdObj, searchVal) => {
        return (searchVal === "" || executionIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEIds = emulationExecutionIds.filter(executionIdObj => {
            return searchFilter(executionIdObj, searchVal)
        });
        setFilteredEmulationExecutionIds(filteredEIds)
        setSearchString(searchVal)
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the monitoring setup
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Real-time monitoring of emulated infrastructures
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Monitoring setup</h4>
                    <p className="modalText">
                        Host and network metrics are collected at each emulated host and sent periodically to a
                        distributed Kafka queue.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Markov chain"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const startOrStopGrafanaRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/grafana' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setGrafanaStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopcAdvisorRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/cadvisor' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setCAdvisorStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopNodeExporterRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/node-exporter' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setNodeExporterStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startOrStopPrometheusRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/prometheus' + "?token=" + props.sessionData.token,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setPrometheusStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchEmulationExecutionIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulation-executions?ids=true' + "&token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                const emulationExecutionIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setEmulationExecutionIds(emulationExecutionIds)
                setFilteredEmulationExecutionIds(emulationExecutionIds)
                setLoading(false)
                if (emulationExecutionIds.length > 0) {
                    setSelectedEmulationExecutionId(emulationExecutionIds[0])
                    fetchSelectedExecution(emulationExecutionIds[0])
                    setLoadingSelectedEmulationExecution(true)
                } else {
                    setLoadingSelectedEmulationExecution(false)
                    setSelectedEmulationExecution(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSelectedExecution = useCallback((id_obj) => {
        fetch(
            (`http://` + ip + ':7777/emulation-executions/' + id_obj.value.id + "?emulation="
                + id_obj.value.emulation + "&token=" + props.sessionData.token),
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setSelectedEmulationExecution(response)
                setLoadingSelectedEmulationExecution(false)
                if (response !== null && response !== undefined) {
                    const containerOptions = response.emulation_env_config.containers_config.containers.map((c, index) => {
                        return {
                            value: c,
                            label: c.full_name_str
                        }
                    })
                    setEmulationExecutionContainerOptions(containerOptions)
                    setSelectedContainer(containerOptions[0])
                    fetchMonitoringData(windowLength.value, response)
                }

            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchMonitoringData = useCallback((len, execution) => fetch(
        (`http://` + ip + ':7777/emulations/' + execution.emulation_env_config.id +
            "/executions/" + execution.ip_first_octet + "/monitor/" + len + "?token=" + props.sessionData.token),
        {
            method: "GET",
            headers: new Headers({
                Accept: "application/vnd.github.cloak-preview"
            })
        }
    )
        .then(res => {
            if(res.status === 401) {
                alert.show("Session token expired. Please login again.")
                props.setSessionData(null)
                navigate("/login-page");
                return null
            }
            return res.json()
        })
        .then(response => {
            if(response === null) {
                return
            }
            setMonitoringData(response)
            setLoadingSelectedEmulationExecution(false)
            var openFlowSwitchesOptions = []
            openFlowSwitchesOptions = Object.keys(response.openflow_port_avg_metrics_per_switch).map((dpid, index) => {
                return {
                    value: dpid,
                    label: dpid
                }
            })
            setOpenFlowSwitchesOptions(openFlowSwitchesOptions)
            if (openFlowSwitchesOptions.length > 0) {
                setSelectedOpenFlowSwitch(openFlowSwitchesOptions[0])
            }
        })
        .catch(error => console.log("error:" + error)), []);


    useEffect(() => {
        setLoading(true)
        fetchEmulationExecutionIds();
    }, []);


    const fetchGrafanaStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/grafana' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setGrafanaStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchGrafanaStatus()
    }, [fetchGrafanaStatus]);


    const fetchCadvisorStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/cadvisor' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setCAdvisorStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchCadvisorStatus()
    }, [fetchCadvisorStatus]);

    const fetchPrometheusStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/prometheus' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setPrometheusStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchPrometheusStatus()
    }, [fetchPrometheusStatus]);

    const fetchNodeExporterStatus = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/node-exporter' + "?token=" + props.sessionData.token,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if(res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                return res.json()
            })
            .then(response => {
                if(response === null) {
                    return
                }
                setNodeExporterStatus(response)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchNodeExporterStatus()
    }, [fetchNodeExporterStatus]);


    const startOrStopGrafana = () => {
        startOrStopGrafanaRequest()
    }

    const startOrStopPrometheus = () => {
        startOrStopPrometheusRequest()
    }

    const startOrStopcAdvisor = () => {
        startOrStopcAdvisorRequest()
    }

    const startOrStopNodeExporter = () => {
        startOrStopNodeExporterRequest()
    }

    const SelectedExecutionView = (props) => {
        if (props.loadingSelectedEmulationExecution || props.selectedEmulationExecution === null || props.selectedEmulationExecution === undefined) {
            if (props.loadingSelectedEmulationExecution) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching execution... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <div className="row">
                        <div className="col-sm-5">
                            <h4>
                                Time-series window length:
                                <div className="conditionalDist inline-block selectEmulation">
                                    <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                        <Select
                                            style={{display: 'inline-block'}}
                                            value={props.windowLength}
                                            defaultValue={props.windowLength}
                                            options={props.windowLengthOptions}
                                            onChange={onChangeWindowLength}
                                            placeholder="Select a window length"
                                        />
                                    </div>
                                </div>
                            </h4>
                        </div>
                        <div className="col-sm-5">
                            <h4>
                                Evolution speed:
                                <div className="conditionalDist inline-block selectEmulation">
                                    <div className="conditionalDist inline-block" style={{width: "300px"}}>
                                        <Select
                                            style={{display: 'inline-block'}}
                                            value={props.animationDuration}
                                            defaultValue={props.animationDuration}
                                            options={props.evolutionSpeedOptions}
                                            onChange={animationDurationUpdate}
                                            placeholder="Set the evolution speed"
                                        />
                                    </div>
                                </div>
                            </h4>
                        </div>
                        <div className="col-sm-2">
                        </div>
                    </div>
                    <AggregateMetrics key={props.animationDuration.value}
                                      loading={props.loadingSelectedEmulationExecution}
                                      animation={props.animation}
                                      animationDuration={props.animationDuration.value}
                                      animationDurationFactor={props.animationDurationFactor}
                                      clientMetrics={getClientMetrics()} snortIdsMetrics={getSnortIdsMetrics()}
                                      aggregatedHostMetrics={getAggregatedHostMetrics()}
                                      aggregatedDockerStats={getAggregatedDockerStats()}
                                      aggregatedOSSECMetrics={getAggregatedOSSECHostMetrics()}
                    />
                    <div className="row hostMetricsDropdownRow">
                        <div className="col-sm-12">
                            <h5 className="text-center inline-block monitoringHeader">
                                <SelectHostDropdownOrSpinner
                                    loading={props.loadingSelectedEmulationExecution}
                                    selectedEmulation={props.selectedEmulationExecution.emulation_env_config}
                                    selectedContainer={props.selectedContainer}
                                    containerOptions={props.emulationExecutionContainerOptions}
                                />
                            </h5>
                        </div>
                    </div>
                    <hr/>

                    <ContainerMetrics key={'container' + '-' + props.animationDuration.value}
                                      loading={props.loadingSelectedEmulationExecution}
                                      hostMetrics={getHostMetrics()}
                                      dockerMetrics={getDockerMetrics()}
                                      ossecAlerts={getOSSECHostMetrics()}
                                      animation={props.animation} animationDuration={props.animationDuration.value}
                                      animationDurationFactor={props.animationDurationFactor}/>

                    <div className="row hostMetricsDropdownRow">
                        <div className="col-sm-12">
                            <h5 className="text-center inline-block monitoringHeader">
                                <SelectOpenFlowSwitchDropdownOrSpinner
                                    loading={props.loadingSelectedEmulationExecution}
                                    selectedEmulation={props.selectedEmulationExecution.emulation_env_config}
                                    selectedSwitch={props.selectedSwitch}
                                    switchesOptions={props.switchesOptions}
                                />
                            </h5>
                        </div>
                    </div>
                    <hr/>
                    <OpenFlowSwitchesStats key={'switch' + '-' + props.animationDuration.value}
                                           loading={props.loadingSelectedEmulationExecution}
                                           portStats={getPortStats()}
                                           flowStats={getFlowStats()}
                                           aggFlowStats={getAggFlowStats()}
                                           animation={props.animation} animationDuration={props.animationDuration.value}
                                           animationDurationFactor={props.animationDurationFactor}/>
                </div>
            )
        }
    }

    const SelectEmulationExecutionIdDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationExecutionIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No running executions are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>)
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching executions... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (<div>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>

                    Selected emulation execution:
                    <div className="conditionalDist inline-block selectEmulation">
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationExecutionId}
                                defaultValue={props.selectedEmulationExecutionId}
                                options={props.emulationExecutionIds}
                                onChange={updateEmulationExecutionId}
                                placeholder="Select an emulation execution"
                            />
                        </div>
                    </div>
                </div>
            )
        }
    }

    const SelectHostDropdownOrSpinner = (props) => {
        if (!props.loading && props.selectedEmulation === null) {
            return (<></>)
        }
        if (props.loading || props.selectedEmulation === null || props.selectedContainer === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <h4>
                        Metrics for Container:
                        <div className="conditionalDist inline-block selectEmulation">
                            <div className="conditionalDist inline-block" style={{width: "500px"}}>
                                <Select
                                    style={{display: 'inline-block', width: "1000px"}}
                                    value={props.selectedContainer}
                                    defaultValue={props.selectedContainer}
                                    options={props.containerOptions}
                                    onChange={updateHost}
                                    placeholder="Select a container from the emulation"
                                />
                            </div>
                        </div>
                    </h4>
                </div>
            )
        }
    }


    const SelectOpenFlowSwitchDropdownOrSpinner = (props) => {
        if (!props.loading && (props.selectedEmulation === null) || props.selectedSwitch === null) {
            return (<></>)
        }
        if (props.loading || props.selectedEmulation === null || props.selectedSwitch === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <h4>
                        Metrics for OpenFlow switch with datapath ID:
                        <div className="conditionalDist inline-block selectEmulation">
                            <div className="conditionalDist inline-block" style={{width: "500px"}}>
                                <Select
                                    style={{display: 'inline-block', width: "1000px"}}
                                    value={props.selectedSwitch}
                                    defaultValue={props.selectedSwitch}
                                    options={props.switchesOptions}
                                    onChange={updateOpenFlowSwitch}
                                    placeholder="Select an OpenFlow switch"
                                />
                            </div>
                        </div>
                    </h4>
                </div>
            )
        }
    }

    const renderStartTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Start service
        </Tooltip>
    );

    const renderStopTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Stop service
        </Tooltip>
    );


    const GrafanaLink = (props) => {
        if (props.grafanaStatus == null || props.grafanaStatus.running === false) {
            return (
                <span className="grafanaStatus">Grafana status: stopped
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStartTooltip()}>
                        <Button variant="success" className="startButton" size="sm"
                                onClick={() => startOrStopGrafana()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.grafanaStatus.url}>Grafana (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="warning" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopGrafana()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const PrometheusLink = (props) => {
        if (props.prometheusStatus == null || props.prometheusStatus.running === false) {
            return (
                <span className="grafanaStatus">Prometheus status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip()}>
                        <Button variant="success" className="startButton" size="sm"
                                onClick={() => startOrStopPrometheus()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.prometheusStatus.url}>Prometheus (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="warning" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopPrometheus()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const NodeExporterLink = (props) => {
        if (props.nodeExporterStatus == null || props.nodeExporterStatus.running === false) {
            return (
                <span className="grafanaStatus">Node exporter status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip()}>
                        <Button variant="success" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopNodeExporter()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.nodeExporterStatus.url}>Node exporter (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="warning" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopNodeExporter()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    const CadvisorLink = (props) => {
        if (props.cAdvisorStatus == null || props.cAdvisorStatus.running === false) {
            return (
                <span className="grafanaStatus">cAdvisor status: stopped
                <OverlayTrigger
                    placement="right"
                    delay={{show: 0, hide: 0}}
                    overlay={renderStartTooltip()}>
                        <Button variant="success" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopcAdvisor()}>
                            <i className="fa fa-play startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </span>)
        } else {
            return (
                <a className="grafanaStatus" href={props.cAdvisorStatus.url}>cAdvisor (running)
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderStopTooltip()}>
                        <Button variant="warning" className="startButton btn-sm" size="sm"
                                onClick={() => startOrStopcAdvisor()}>
                            <i className="fa fa-stop-circle-o startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </a>
            )
        }
    }

    return (
        <div className="container-fluid">
            <h3 className="managementTitle"> Monitoring of Emulations </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectEmulationExecutionIdDropdownOrSpinner
                            loading={loading} emulationExecutionIds={filteredEmulationExecutionIds}
                            selectedEmulationExecutionId={selectedEmulationExecutionId}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
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
                <div className="col-sm-1">
                </div>
            </div>
            <SelectedExecutionView loadingSelectedEmulationExecution={loadingSelectedEmulationExecution}
                                   selectedEmulationExecution={selectedEmulationExecution}
                                   windowLength={windowLength}
                                   windowLengthOptions={windowLengthOptions}
                                   animationDuration={animationDuration}
                                   evolutionSpeedOptions={evolutionSpeedOptions}
                                   selectedContainer={selectedContainer}
                                   emulationExecutionContainerOptions={emulationExecutionContainerOptions}
                                   animationDurationFactor={animationDurationFactor}
                                   animation={animation}
                                   selectedSwitch={selectedOpenFlowSwitch}
                                   switchesOptions={openFlowSwitchesOptions}
            />
            <div className="row">
                <div className="col-sm-12">
                    <GrafanaLink className="grafanaStatus" grafanaStatus={grafanaStatus}/>
                    <PrometheusLink className="grafanaStatus" prometheusStatus={prometheusStatus}/>
                    <NodeExporterLink className="grafanaStatus" nodeExporterStatus={nodeExporterStatus}/>
                    <CadvisorLink className="grafanaStatus" cAdvisorStatus={cAdvisorStatus}/>
                </div>
            </div>
        </div>
    );
}

Monitoring.propTypes = {};
Monitoring.defaultProps = {};
export default Monitoring;