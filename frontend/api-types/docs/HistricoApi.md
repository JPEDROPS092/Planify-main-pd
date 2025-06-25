# HistricoApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**documentsHistoricoList**](#documentshistoricolist) | **GET** /api/documents/historico/ | Listar histórico de alterações de documentos|
|[**documentsHistoricoRetrieve**](#documentshistoricoretrieve) | **GET** /api/documents/historico/{id}/ | Detalhes de um registro de histórico|

# **documentsHistoricoList**
> PaginatedHistoricoDocumentoList documentsHistoricoList()

Retorna a lista de todas as alterações registradas para os documentos.

### Example

```typescript
import {
    HistricoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new HistricoApi(configuration);

let alteradoPor: number; //Filtrar por ID do usuário que realizou a alteração (optional) (default to undefined)
let documento: number; //Filtrar por ID do documento (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.documentsHistoricoList(
    alteradoPor,
    documento,
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alteradoPor** | [**number**] | Filtrar por ID do usuário que realizou a alteração | (optional) defaults to undefined|
| **documento** | [**number**] | Filtrar por ID do documento | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedHistoricoDocumentoList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Lista de histórico de documentos recuperada com sucesso |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsHistoricoRetrieve**
> HistoricoDocumento documentsHistoricoRetrieve()

Retorna os detalhes de um registro específico do histórico de alterações de um documento.

### Example

```typescript
import {
    HistricoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new HistricoApi(configuration);

let id: number; //A unique integer value identifying this Histórico de Documento. (default to undefined)

const { status, data } = await apiInstance.documentsHistoricoRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Histórico de Documento. | defaults to undefined|


### Return type

**HistoricoDocumento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Detalhes do registro de histórico recuperados com sucesso |  -  |
|**404** | Registro de histórico não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

