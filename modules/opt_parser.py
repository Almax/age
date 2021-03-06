#  parse user-input options

import argparse

def opts_to_string(opts_lst):

    opts_str = ''
    for opt_name, opt in opts_lst:
        if not isinstance(opt, dict):
            opt = vars(opt)
        opts_str += (opt_name + '\n')
        opts_str += '\n'.join(['  %-20s: %s' % (k,v) for k,v in opt.iteritems()])
        opts_str += '\n\n'
    return opts_str


def parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type = str, default = 'help',
        choices = ['train', 'test', 'finetune','train_video', 'finetune_video', 'test_video', 'help'], help = 'valid commands: train, test, help')

    command = parser.parse_known_args()[0].command

    return command

def parse_opts_joint_model():
    parser = argparse.ArgumentParser()

    # common
    parser.add_argument('--cnn', type = str, default = 'resnet18', choices = ['resnet18', 'resnet50', 'vgg16'],
        help = 'cnn network')

    parser.add_argument('--feat_size', type = int, default = 256,
        help = 'feature size of embedding space')

    parser.add_argument('--num_cls_layer', type = int, default = 2, choices = [1,2],
        help = 'number of fc layers in classifiers (inlcuding age, pose and attribute)')

    parser.add_argument('--cls_mid_size', type = int, default = 128, 
        help = 'middle fc layer output size of classifiers')

    parser.add_argument('--dropout', type = float, default = 0,
        help = 'dropout rate')

    # age
    parser.add_argument('--min_age', type = int, default = 0,
        help = 'min age')

    parser.add_argument('--max_age', type = int, default = 70,
        help = 'max age')

    parser.add_argument('--cls_type', type = str, default = 'oh', choices = ['oh', 'dex'],
        help = 'oh: ordinal hyperplane; dex: deep expectation')

    parser.add_argument('--oh_relaxation', type = int, default = 3,
        help = 'relaxation parameter of ordinal hyperplane loss')

    
    # pose
    parser.add_argument('--pose_cls', type = int, default = 1, choices = [0, 1],
        help = 'whether has pose classifier [0-no | 1-yes]')

    parser.add_argument('--pose_dim', type = int, default = 2, choices = [1, 2],
        help = 'number of pose axes [1-only yaw | 2-yaw and pitch]')


    # attribute
    parser.add_argument('--attr_cls', type = int, default = 1, choices = [0, 1],
        help = 'whether has attribute classifier [0-no | 1-yes]')

    parser.add_argument('--num_attr', type = int, default = 40,
        help = 'number of attributes, 40 for celeba, 6 for celeba_selc1')

    parser.add_argument('--attr_name_fn', type = str, default = 'datasets/CelebA/Label/attr_name_lst.txt',
        help = 'attribute name list file')

    parser.add_argument('--attr_share_fc', type = int, default = 0, choices = [0,1],
        help = 'pose and attribute branchs share the fc layer')


    opts = parser.parse_known_args()[0]
    return opts

def parse_opts_pose_model():

    parser = argparse.ArgumentParser()

    parser.add_argument('--cnn', type = str, default = 'resnet18', choices = ['resnet18', 'resnet50', 'vgg16'],
        help = 'cnn network')

    parser.add_argument('--num_fc', type = int, default = 1, choices = [0, 1],
        help = 'number of fc layers in classifier')

    parser.add_argument('--fc_sizes', type = int, default = [256], nargs = '*',
        help = 'size of intermediate fc layers')

    parser.add_argument('--pose_dim', type = int, default = 1, choices = [1, 2],
        help = '1-only yaw; 2-yaw and pitch')

    parser.add_argument('--dropout', type = float, default = 0,
        help = 'dropout rate')

    parser.add_argument('--output_norm', type = int, default = 0, choices = [0, 1])

    opts = parser.parse_known_args()[0]
    return opts


def parse_opts_attribute_model():

    parser = argparse.ArgumentParser()

    parser.add_argument('--cnn', type = str, default = 'resnet18', choices = ['resnet18', 'resnet50', 'vgg16'],
        help = 'cnn network')

    parser.add_argument('--num_fc', type = int, default = 1, choices = [0, 1],
        help = 'number of fc layers in classifier')

    parser.add_argument('--fc_sizes', type = int, default = [256], nargs = '*',
        help = 'size of intermediate fc layers')

    parser.add_argument('--num_attr', type = int, default = 40,
        help = 'number of attributes, 40 for celeba, 6 for celeba_selc1')

    parser.add_argument('--attr_name_fn', type = str, default = 'datasets/CelebA/Label/attr_name_lst.txt',
        help = 'attribute name list file')

    parser.add_argument('--dropout', type = float, default = 0,
        help = 'dropout rate')

    opts = parser.parse_known_args()[0]
    return opts

def parse_opts_age_model():

    parser = argparse.ArgumentParser()

    parser.add_argument('--cnn', type = str, default = 'resnet18', choices = ['resnet18', 'resnet50', 'vgg16'],
        help = 'cnn network')

    parser.add_argument('--min_age', type = int, default = 0,
        help = 'min age')

    parser.add_argument('--max_age', type = int, default = 70,
        help = 'max age')

    parser.add_argument('--num_fc', type = int, default = 1, choices = [1, 2],
        help = 'number of fc layers in classifier')

    parser.add_argument('--fc_sizes', type = int, default = [256],
        help = 'size of intermediate fc layers')

    parser.add_argument('--cls_type', type = str, default = 'oh', choices = ['oh', 'dex'],
        help = 'oh: ordinal hyperplane; dex: deep expectation')

    parser.add_argument('--oh_relaxation', type = int, default = 3,
        help = 'relaxation parameter of ordinal hyperplane loss')

    parser.add_argument('--dropout', type = float, default = 0,
        help = 'dropout rate')

    opts = parser.parse_known_args()[0]
    return opts


def parse_opts_train():
    parser = argparse.ArgumentParser()

    # basic
    parser.add_argument('--id', type = str, default = 'default',
        help = 'model id')

    parser.add_argument('--gpu_id', type = int, default = [0], nargs = '*',
        help = 'GPU device id used for model training')

    parser.add_argument('--debug', type = int, default = 0,
        help = 'use a small set of data to debug model')

    parser.add_argument('--pavi', type = int, default = 1, choices = [0, 1],
        help = 'use pavi log')
    

    # data
    parser.add_argument('--dataset', type = str, default = 'video_age',
        choices = ['imdb_wiki', 'imdb_wiki_good', 'megaage', 'morph', 'lap', 'video_age'],
        help = 'dataset name [imdb_wiki|imdb_wiki_good|megaage|morph|lap|video_age]')

    parser.add_argument('--face_alignment', type = str, default = '21',
        choices = ['3', '21', 'none'],
        help = 'face alignment mode. see prepro_general for more information')

    parser.add_argument('--crop_size', type = int, default = 128,
        help = 'center crop size')

    # for video age dataset
    parser.add_argument('--dataset_version', type = str, default = '2.0',
        choices = ['1.0', '2.0'],
        help = 'video_age dataset version')

    parser.add_argument('--train_split', type = str, default = '',
        choices = ['0.1', '0.2', '0.5', ''],
        help = 'video_age dataset training split')

    parser.add_argument('--video_max_len', type = int, default = 17,
        help = 'max frame number in each video sample')


    
    # optimization
    parser.add_argument('--max_epochs', type = int, default = 30,
        help = 'number of training epochs')

    parser.add_argument('--batch_size', type = int, default = 32,
        help = 'batch size')

    parser.add_argument('--clip_grad', type = float, default = -1,
        help = 'clip gradient by L2 norm')

    parser.add_argument('--optim', type = str, default = 'sgd',
        choices = ['sgd', 'adam'])

    parser.add_argument('--lr', type = float, default = 1e-3,
        help = 'learning rate')

    parser.add_argument('--lr_decay', type = int, default = 10,
        help = 'every how many epochs does the learning rate decay')

    parser.add_argument('--lr_decay_rate', type = float, default = 0.1,
        help = 'learning decay rate')

    parser.add_argument('--weight_decay', type = float, default = 5e-4,
        help = 'L2 weight decay')

    parser.add_argument('--momentum', type = float, default = 0.9,
        help = 'momentum for SGD')

    parser.add_argument('--optim_alpha', type = float, default = 0.9,
        help = 'alpha for adam')

    parser.add_argument('--optim_beta', type = float, default = 0.999,
        help = 'beta for adam')

    parser.add_argument('--optim_epsilon', type = float, default = 1e-8,
        help = 'epsilon that goes into denominator for smoothing')

    parser.add_argument('--display_interval', type = int, default = 10,
        help = 'every how many batchs display training loss')

    parser.add_argument('--test_interval', type = int, default = 1,
        help = 'every how many epochs do test')

    parser.add_argument('--test_iter', type = int, default = -1,
        help = 'test iterations. -1 means useing all samples in test set')

    parser.add_argument('--snapshot_interval', type = int, default = 10,
        help = 'every how many epochs save model parameters to file')

    parser.add_argument('--average_loss', type = int, default = -1, 
        help = 'average the last n loss when display')

    parser.add_argument('--cls_lr_multiplier', type = float, default = 10,
        help = 'learning rate multiplier of the classifier layers')

    parser.add_argument('--loss_sample_normalize', type = int, default = 1,
        help = 'for oh loss, 1 means averaging loss over samples, 0 means averaging loss over channels')


    # finetune
    parser.add_argument('--pre_id', type = str, default = ['models/age_pre_2.2/9.pth', 'models/joint_1.13/23.pth'], nargs = '*',
        help = 'the list of pretrained model IDs (or model files if end with ".pth")')

    parser.add_argument('--only_load_cnn', type = int, default = 1, choices = [0, 1],
        help = '0-load pretrained weights for all layers, 1-load pretrained weights only for CNN')
    
    # joint training
    parser.add_argument('--train_cnn', type = int, default = 1, choices = [0, 1],
        help = 'whether optimize cnn parameters')

    parser.add_argument('--train_embed', type = int, default = 1, choices = [0, 1],
        help = 'whether optimize feature embedding layer parameters')

    parser.add_argument('--train_pose', type = int, default = 1, choices = [0, 1],
        help = 'whether optimize pose classifier parameters [0-no | 1-yes]')

    parser.add_argument('--train_attr', type = int, default = 1, choices = [0, 1],
        help = 'whether optimize attribute classifier parameters [0-no | 1-yes]')

    parser.add_argument('--loss_weight_age', type = float, default = 1,
        help = 'age loss weight')

    parser.add_argument('--loss_weight_pose', type = float, default = 0.2,
        help = 'pose loss weight')

    parser.add_argument('--loss_weight_attr', type = float, default = 10,
        help = 'attribute loss weight')

    parser.add_argument('--batch_size_pose', type = int, default = 128,
        help = 'pose sample batch size')

    parser.add_argument('--batch_size_attr', type = int, default = 128,
        help = 'attribute sample batch size')

    parser.add_argument('--sidetask_lr_multiplier', type = float, default = 1.0,
        help = 'learning rate multiplier of layers: feat_embed, pose_cls, attr_cls')

    parser.add_argument('--attr_dataset', type = str, default = 'celeba',
        choices = ['celeba', 'celeba_selc1'],
        help = 'dataset for attribute recognition')

    parser.add_argument('--adjust_weight_decay', type = int, default = 0,
        help = 'adjust weight decay w.r.t. loss weight')

    parser.add_argument('--lr_decay_pose', type = int, default = -1,
        help = 'specilize learning rate decay for pose branch')

    # perturbation
    parser.add_argument('--pert_enable', type = int, default = 0, choices = [0, 1],
        help = 'enable feature perturbation')

    parser.add_argument('--loss_weight_pert', type = float, default = 1.0,
        help = 'perturbation loss weight')

    parser.add_argument('--pert_mode', type = str, default = 'age_embed_L2',
        choices = ['age_embed_L2', 'age_embed_cos'],
        help = 'perturbation method')

    parser.add_argument('--pert_start_time', type = int, default = 1,
        help = 'enable perturbation after a number of training epochs')

    parser.add_argument('--pert_guide_signal', type = str, default = 'pose', 
        choices = ['pose', 'attr'],
        help = 'type of perturbation guidance signal')

    parser.add_argument('--pert_guide_index', type = int, default = 0,
        help = 'output index of perturbation guidance signal')

    parser.add_argument('--pert_scale', type = float, default = 0.05,
        help = 'perturbation scale')




    opts = parser.parse_known_args()[0]
    return opts


def parse_opts_test():

    parser = argparse.ArgumentParser()

    # basic
    parser.add_argument('--id', type = str, default = None,
        help = 'model id or model file if end with .pth')

    parser.add_argument('--gpu_id', type = int, default = [0], nargs = '*',
        help = 'GPU device id used for model training')

    parser.add_argument('--output_rst', type = int, default = 1, choices = [0, 1],
        help = 'output predicted age of each sample to a pkl file')

    parser.add_argument('--output_feat', type = int, default = 1, choices = [0,1],
        help = 'output feature of each sample to a h5 file')

    # data
    parser.add_argument('--dataset', type = str, default = 'imdb_wiki_good',
        choices = ['imdb_wiki', 'imdb_wiki_good', 'megaage', 'morph', 'lap', 'video_age'],
        help = 'dataset name [imdb_wiki|imdb_wiki_good|megaage|morph|lap|video_age]')

    parser.add_argument('--dataset_version', type = str, default = '2.0',
        choices = ['1.0', '2.0'],
        help = 'video_age dataset version')

    parser.add_argument('--subset', type = str, default = 'test',
        choices = ['train', 'test', 'val'],
        help = 'subset of the dataset')

    parser.add_argument('--face_alignment', type = str, default = '21',
        choices = ['3', '21', 'none'],
        help = 'face alignment mode. see prepro_general for more information')

    parser.add_argument('--batch_size', type = int, default = 128,
        help = 'batch size')

    parser.add_argument('--crop_size', type = int, default = 128,
        help = 'center crop size')

    opts = parser.parse_known_args()[0]
    return opts
    






if __name__ == '__main__':

    # test parse_command()

    command = parse_command()

    print(command)