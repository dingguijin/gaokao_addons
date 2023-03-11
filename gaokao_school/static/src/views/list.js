import { listView } from "@web/views/list/list_view";
import { registry } from '@web/core/registry';

registry.category('views').add('gaokao_school_tree', {
    ...listView,
    buttonTemplate: 'gaokao.ListButtons',
});

